#-------------------------------------------------------------------------
# Copyright (c) DSL
# All rights reserved.
#
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#--------------------------------------------------------------------------

"""
    Supports publishing and consuming published services that execute within the BuaBuaML
    web service execution framework.

    Existing services can be consumed using the service decorator:
    
        from buabuaml import services
        
        @services.service(url, api_key)
        @services.types(a = float, b = float)
        @services.returns(float)
        def some_service(a, b):
            pass

Where the url and api_key are specified for the published web service.  

        Python functions can be published using the @publish decorator:
        
            @services.publish(workspace, workspace_key)
            @services.types(a = float, b = float)
            @services.returns(float)
            def float_typed(a, b):
                return a / b

        The function will be published under a newly created endpoint.

        Publish can also be called programmatically instead:
        
            published = services.publish(myfunc2, workspace, workspace_key)

    The types and returns decorators can be used to provide type information about the
    inputs and outputs.  These types will be visible on the help page and enable clients
    written in other languages to call published Python functions.
    
    If types aren't specified then core Python types will be serialized in a custom manner.
    This allows working with many common types such as lists, dictionaries, numpy types, etc...
    But interop with other languages will be much more difficult.


    Files can also be attached to published functions using the @attach decorator:

        @services.publish(workspace, workspace_key)
        @services.attach('foo.txt')
        def attached():
            return ''.join(file('foo.txt').readlines())

"""
import sys
from functools import update_wrapper


import codecs
import inspect
import dis 

import re
import requests
import uuid
import json
import base64
import zipfile

from collections import deque, OrderedDict

from types import CodeType, FunctionType, ModuleType
import types as typesmod

try:
    import cPickle as pickle
except:
    import pickle
    
try:
    from io import BytesIO
except:
    from cStringIO import StringIO as BytesIO
    
try:
    import buabuaml
except:
    # We are published, we won't call publish_worker again.
    pass

try:
    import numpy
except:
    numpy = None

try:
    import pandas
except:
    pandas = None

_LOAD_GLOBAL = dis.opmap['LOAD_GLOBAL']
#################################################
# Serialization/Deserialization of inputs.  This code is distinct from the
# serialization of the user defined function.  The user defined function can contain
# arbitrary objects and is fully trusted (so we can use pickle).  The inputs to the function 
# are coming from arbitrary user input and so need to support a more limited form
# of serialization.
# 
# Serialization of the arguments is done using JSON.  Each argument is serialized with
# a type and a value.  The type is a known type name (int, bool, float, etc...) and the
# value is the serialized value in string format.  Usually this is the simplest possible
# representation.  Strings are serialized as is, ints/floats we just call str() on, etc...
# For byte arrays we base64 encode them.  For data structures we store a list of the elements
# which are encoded in the same way.  For example a list would have a list of dictionaries
# in JSON which each have a type and value member.
#
_serializers = {}
_deserializers = {}

#
def serializer(type):
    def l(func):
        _serializers[type] = func
        return func
    return l

def deserializer(type):
    def l(func):
        _deserializers[type] = func
        return func
    return l

# Type: bool
@serializer(bool)
def _serialize_bool(inp, memo):
    return {'type': 'bool', 'value': 'true' if inp else 'false' }

@deserializer('bool')
def _deserialize_bool(value):
    if value['value'] == 'true':
        return True
    else:
        return False

# Type: int
@serializer(int)
def _serialize_int(inp, memo):
    return {'type': 'int', 'value': str(inp) }

@deserializer('int')
def _deserialize_int(value):
    return int(value['value'])

if sys.version_info < (3, ):
    # long
    @serializer(long)
    def _serialize_long(inp, memo):
        return {'type': 'long', 'value': str(inp) }

    @deserializer('long')
    def _deserialize_long(value):
        return long(value['value'])

# Type: float
@serializer(float)
def _serialize_float(inp, memo):
    return {'type': 'float', 'value': str(inp) }

@deserializer('float')
def _deserialize_float(value):
    return float(value['value'])


# Type: complex
@serializer(complex)
def _serialize_complex(inp, memo):
    return {'type': 'complex', 'value': str(inp) }

@deserializer('complex')
def _deserialize_bool(value):
    return complex(value['value'])


# Type: unicode
@serializer(str if sys.version_info >= (3,) else unicode)
def _serialize_unicode(inp, memo):
    return {'type': 'unicode', 'value': str(inp) }

@deserializer('unicode')
def _deserialize_unicode(value):
    return value['value']


# Type: byte arrays
@serializer(bytes if sys.version_info >= (3,) else str)
def _serialize_bytes(inp, memo):
    data = base64.encodestring(inp)
    if sys.version_info >= (3, ):
        data = data.decode('utf8')
    return {'type': 'bytes', 'value': data.replace(chr(10), '') }

@deserializer('bytes')
def _deserialize_bytes(value):
    data = value['value']
    if sys.version_info >= (3, ):
        data = data.encode('utf8')
    return base64.decodestring(data)

# Type: dictionaries
@serializer(dict)
def serialize_dict(inp, memo):
    return  {
        'type': 'dict', 
        'value' : [(_encode(k, memo), _encode(inp[k], memo)) for k in inp]
    }
    

@deserializer('dict')
def _deserialize_dict(value):
    return { _decode_inner(k):_decode_inner(v) for k, v in value['value'] }

# Type: None/null

@serializer(type(None))
def serialize_none(inp, memo):
    return {'type':'null', 'value':'null'}

@deserializer('null')
def _deserialize_null(value):
    return None


# Type: list and tuple
@serializer(list)
@serializer(tuple)
def _serialize_list_or_tuple(inp, memo):
    res = []
    for value in inp:
        res.append(_encode(value, memo))

    return {'type': type(inp).__name__, 'value': res }

@deserializer('list')
def _deserialize_list(value):
    return [_decode_inner(x) for x in value['value']]

@deserializer('tuple')
def _deserialize_tuple(value):
    return tuple(_decode_inner(x) for x in value['value'])


if numpy is not None:
    # ndarray is serialized as (shape, datatype, data)
    @serializer(numpy.ndarray)
    def serialize_ndarray(inp, memo):
        return {
            'type':'numpy.ndarray', 
            'value': (
                _encode(inp.shape, memo), 
                _encode(inp.dtype.name, memo), 
                _encode(inp.tostring(), memo)
            )
        }

    @deserializer('numpy.ndarray')
    def deserialize_ndarray(value):
        shape, dtype, data = value['value']
        return numpy.ndarray(
            _decode_inner(shape), _decode_inner(dtype), _decode_inner(data)
        )

    # TODO: Need better story here...
    @serializer(numpy.int32)
    def serialize_numpy_int32(inp, memo):
        return _serialize_int(inp, memo)

    @serializer(numpy.int64)
    def serialize_numpy_int64(inp, memo):
        if sys.version_info >= (3, ):
            return _serialize_int(inp, memo)

        return _serialize_long(inp, memo)

    @serializer(numpy.float64)
    def serialize_numpy_float64(inp, memo):
        return _serialize_float(inp, memo)

# Core deserialization functions.  There's a top-level one used when
# actually reading/writing values, and an inner one when we're doing the
# recursive serialization/deserialization.

def _decode_inner(value):
    val_type = value['type']
    deserializer = _deserializers.get(value['type'])
    if deserializer is None:
        raise ValueError("unsupported type: " + value['type'])
    
    return deserializer(value)

def _encode(inp, memo = None):
    outer = False
    if memo is None:
        outer = True
        memo = {}
    if id(inp) in memo and type(inp) in [list, tuple, dict]:
        raise ValueError('circular reference detected')
    memo[id(inp)] = inp

    serializer = _serializers.get(type(inp))
    if serializer is None:
        raise TypeError("Unsupported type for invocation: " + type(inp).__module__ + '.' + type(inp).__name__)

    res = serializer(inp, memo)
    if outer:
        return json.dumps(res)
    return res


def _decode(inp):
    value = json.loads(inp)

    if isinstance(value, dict):
        return _decode_inner(value)

    raise TypeError('expected a dictionary, got ' + type(inp).__name__)

SWAGGER_URL_FORMAT = '/workspaces/{}/services/{}/{}'
PUBLISH_URL_FORMAT = '{}/{}/workspaces/{}/services/{}/{}'

if sys.version_info >= (3, 0):
    _code_args = ['co_argcount', 'co_kwonlyargcount', 'co_nlocals', 'co_stacksize', 'co_flags', 
                  'co_code', 'co_consts',  'co_names', 'co_varnames', 'co_filename', 'co_name', 
                  'co_firstlineno', 'co_lnotab', 'co_freevars', 'co_cellvars']
    _func_args = ['__name__', '__defaults__', '__closure__']
else:
    _code_args = ['co_argcount', 'co_nlocals', 'co_stacksize', 'co_flags', 'co_code', 'co_consts', 
                  'co_names', 'co_varnames', 'co_filename', 'co_name', 'co_firstlineno', 'co_lnotab',
                  'co_freevars', 'co_cellvars']
    _func_args = ['func_name', 'func_defaults', 'func_closure']


class _Serializer(object):
    '''serializes the specified functions, and the globals it uses as well.

normal globals are just serialized as-is, they must be picklable to do so.

other functions which are referenced are serialized as an additional function, and
will be repopulated in globals.  This allows things like mutually recursive functions
to exist.
'''    
    def __init__(self):
        self.functions = set()
        self.queue = deque()

    if sys.version_info < (3, ):
        CLASS_TYPES = (typesmod.ClassType, type)
    else:
        CLASS_TYPES = type
    
    def serialize(self, obj):
        self.queue.append(('func', obj.__name__, obj))
        self.functions.add((obj.__name__, obj))
        self.mod = obj.__module__

        return self.serialize_obj(obj)

    def serialize_obj(self, obj):
        res = []
        while self.queue:
            objType, name, cur = self.queue.popleft()

            if objType == 'func':
                res.append((objType, name, self.get_code_args(cur)))
            elif objType == 'mod':
                res.append((objType, name, cur.__name__))
            elif objType == 'type':
                raise NotImplementedError('new style class not supported')
            elif objType == 'oldclass':
                res.append((objType, name, [cur.__name__, cur.__module__, cur.__bases__, {n:self.serialize_obj(v) for n, v in cur.__dict__.items()}]))
            else:
                raise Exception('Unknown serialization type')

        return pickle.dumps(res)

    @staticmethod
    def find_globals(code):
        """walks the byte code to find the variables which are actually globals"""
        cur_byte = 0
        byte_code = code.co_code
        
        names = set()
        while cur_byte < len(byte_code):
            op = ord(byte_code[cur_byte])

            if op >= dis.HAVE_ARGUMENT:
                if op == _LOAD_GLOBAL:
                    oparg = ord(byte_code[cur_byte + 1]) + (ord(byte_code[cur_byte + 2]) << 8)
                    name = code.co_names[oparg]
                    names.add(name)

                cur_byte += 2
            cur_byte += 1
        
        return names

    def get_code_args(self, func):
        code = func.__code__
    
        codeArgs = [getattr(code, name) for name in _code_args]
        funcArgs = [getattr(func, name) for name in _func_args]
        globals = {}
    
        for name in self.find_globals(code):
            if name in func.__globals__:
                value = func.__globals__[name]
                if isinstance(value, FunctionType):
                    if (name, value) not in self.functions:
                        self.queue.append(('func', name, value))
                        self.functions.add((name, value))
                elif isinstance(value, ModuleType):
                    self.queue.append(('mod', name, value))
                elif isinstance(value, _Serializer.CLASS_TYPES) and  value.__module__ == self.mod:
                    # class that needs to be serialized...
                    if isinstance(value, type):
                        # new-style class
                        self.queue.append(('type', name, value))
                    else:
                        # old-style class
                        self.queue.append(('oldclass', name, value))
                else:
                    globals[name] = value

        return pickle.dumps((codeArgs, funcArgs, globals))

def _serialize_func(func): 
    return _Serializer().serialize(func)

def _deserialize_func(funcs, globalDict):
    items = pickle.loads(funcs)
    res = None
    for objType, name, data in items:
        if objType == 'func':
            codeArgs, funcArgs, updatedGlobals = pickle.loads(data)
            code = CodeType(*codeArgs)    
    
            globalDict.update(**updatedGlobals)

            value = FunctionType(code, globalDict, *funcArgs)
        elif objType == 'mod':
            value = __import__(data)
        elif objType == 'oldclass':
            class_name, module, bases, class_dict = data
            value = typesmod.ClassType(class_name, bases, {k:_deserialize_func(v, globalDict) for k, v in class_dict.items()})
            value.__module__ = module
        elif objType == 'type':
            raise Exception('deserialize type')
        else:
            raise Exception('Unknown serialization type')
        globalDict[name] = value

        if res is None:
            res = value

    return res

def _get_args(func):
    raw_schema = _get_dataframe_schema(func)
    if raw_schema is not None:
        return list(raw_schema.keys())
    
    args = inspect.getargs(func.__code__)
    all_args = args.args
    if args.varargs is not None:
        all_args.append(args.varargs)
    if args.keywords is not None:
        all_args.append(args.keywords)
    return all_args

def _encode_arg(arg, type):
    if type == OBJECT_NAME:
        return _encode(arg)
    elif type['type'].lower() == 'string':
        return arg

    return json.dumps(arg)

def _decode_one_response(response, real_type):
    if real_type == OBJECT_NAME:
        return _decode(response[0])
    elif real_type['type'].lower() == 'string':
        return response[0]
    
    # TODO: These shouldn't be necessary, BuaBuaML is returning things to us oddly...
    if response[0] == 'True':
        return True
    elif response[0] == 'False':
        return False
    return json.loads(response[0])

def _get_dict_type(column, index, type, types):
    if type is not None and column in type:
        return _annotation_to_type(type[column])

    return {'type': types[index]}

def _decode_response(columns, types, response, type):
    if isinstance(type, tuple):
        # multi-value decode...
        return tuple(_decode_one_response((r, ), _annotation_to_type(t)) for r, t in zip(response, type))
    elif isinstance(type, dict):
        return {c:_decode_one_response((r, ), _get_dict_type(c, i, type, types)) for (i, c), r in zip(enumerate(columns), response)}
    elif columns is not None and len(columns) > 1:
        return {c:_decode_one_response((r, ), {'type': types[i]}) for (i, c), r in zip(enumerate(columns), response)}

    return _decode_one_response(response, _annotation_to_type(type))

        
class published(object):
    """The result of publishing a service or marking a method as being published.

Supports being called to invoke the remote service, iteration for unpacking the url,
api key, and help url, or the url, api_key, and help_url can be accessed directly
as attributes.
"""

    def __init__(self, url, api_key, help_url, func, service_id):
#        self.url = url
        self.url = url
        self.api_key = api_key
        self.help_url = help_url
        self.func = func
        self.service_id = service_id

    def __repr__(self):
        return '<service {} at {}>'.format(self.func.__name__, self.url)

    def _invoke(self, call_args):
        body = {
            "Inputs": {
                getattr(self.func, '__input_name__', 'input1'): {
                    "ColumnNames": _get_args(self.func),
                    "Values": call_args,
                }
            },
            "GlobalParameters": {}
        }

        resp = requests.post(
            self.url, 
            json=body, 
            headers={
            'authorization': 'bearer ' + self.api_key,
            }
        )
        
        r = resp.json()
        if resp.status_code >= 300:
            try:
                code = r['error']['code']
            except LookupError:
                code = None
            if code in ('ModuleExecutionError', 'Unauthorized'):
                raise RuntimeError(r['error']['details'][0]['message'])
            raise ValueError(str(r))
        return r

    def _map_args(self, *args, **kwargs):
        args = inspect.getcallargs(self.func, *args, **kwargs)
        return [ _encode_arg(args[name], _get_arg_type(name, self.func)) for name in _get_args(self.func) ]

    def __call__(self, *args, **kwargs):
        
        return "__call__"
        # Call remote function
        r = self._invoke([ self._map_args(*args, **kwargs) ])
        output_name = getattr(self.func, '__output_name__', 'output1')
        return _decode_response(
            r["Results"][output_name]["value"].get("ColumnNames"),
            r["Results"][output_name]["value"].get("ColumnTypes"),
            r["Results"][output_name]["value"]["Values"][0], 
            _get_annotation('return', self.func)
        )

    def map(self, *args):
        """maps the function onto multiple inputs.  The input should be multiple sequences.  The
sequences will be zipped together forming the positional arguments for the call.  This is
equivalent to map(func, ...) but is executed with a single network call."""
        call_args = [self._map_args(*cur_args)  for cur_args in zip(*args)]
        r = self._invoke(call_args)

        ret_type = _get_annotation('return', self.func)
        output_name = getattr(self.func, '__output_name__', 'output1')
        return [_decode_response(
                    r['Results'][output_name]['value'].get("ColumnNames"), 
                    r['Results'][output_name]['value'].get("ColumnTypes"), 
                    x, 
                    ret_type) 
                for x in r['Results']['output1']['value']['Values']]

    def delete(self):
        """unpublishes the service"""
        raise NotImplementedError('delete not implemented yet')

    def __iter__(self):
        yield self.url
        yield self.api_key
        yield self.help_url


def _get_dataframe_schema(function):
    return getattr(function, '__dataframe_schema__', None)

def _get_main_source(function):
    
    main_source = u'def buabuaml_main(df1 = None, df2 = None):\n'
    main_source += u'    results = []\n' 

    if _get_dataframe_schema(function):
        # function just takes a dataframe...
        main_source += u'    results.append(__user_function(df1))' + chr(10)
    else:
        # we're marshalling the arguments in.
        main_source += u'    for i in range(df1.shape[0]):' + chr(10)
        for arg in _get_args(function):
            arg_type = _get_arg_type(arg, function)
            if pandas is not None and arg_type is pandas.DataFrame:
                raise Exception('Only a single DataFrame argument is supported')

            if _get_arg_type(arg, function) == OBJECT_NAME:
                main_source += '        ' + arg + u' = ' + u'_decode(df1["' + arg + u'"][i])' + chr(10)
            else:
                main_source += '        ' + arg + u' = ' + u'df1["' + arg + u'"][i]' + chr(10)
    
        main_source += u'        results.append(__user_function(' 
    
        args = inspect.getargs(function.__code__)
        all_args = args.args
        if args.varargs is not None:
            all_args.append(u'*' + args.varargs)
        if args.keywords is not None:
            all_args.append(u'**' + args.keywords)
    
        # pass position arguments...
        main_source += u', '.join(all_args)
        main_source += u'))' + chr(10)
    
    ret_annotation = _get_annotation('return', function)
    if _get_dataframe_schema(function):
        # function just returns a data frame directly
        main_source += u'    if len(results) == 1:' + chr(10)
        main_source += u'        return results[0]' + chr(10)
        main_source += u'    return pandas.DataFrame(results)' + chr(10)
    elif isinstance(ret_annotation, tuple):
        # multi-value return support...
        format = []
        arg_names = []
        for index, ret_type in enumerate(ret_annotation):
            arg_names.append(u'r' + str(index))
            t = _annotation_to_type(ret_type)
            if t == OBJECT_NAME:
                format.append(u'_encode(r' + str(index) + u')')
            else:
                format.append(u'r' + str(index))
        main_source += u'    return pandas.DataFrame([(' + u', '.join(format) + u') for ' + ', '.join(arg_names) + u' in results])' + chr(10)
    elif _get_arg_type('return', function) == OBJECT_NAME:
        main_source += u'    return pandas.DataFrame([_encode(r) for r in results])' + chr(10)
    else:
        main_source += u'    return pandas.DataFrame(results)' + chr(10)
    
    return main_source

def _get_source(function):
    source_file = inspect.getsourcefile(function)
    encoding = ''
    try:
        with open(source_file, 'rb') as source_file:
            line1 = source_file.readline()
            line2 = source_file.readline()
            if line1[:3] == '\xef\xbb\xbf':
                encoding = 'utf-8-sig'
            else:
                match = re.search(b"coding[:=]\s*([-\w.]+)", line1) or re.search(b"coding[:=]\s*([-\w.]+)", line2)
                if match:
                    encoding = match.groups()[0]
        with codecs.open(source_file, 'r', encoding) as source_file:
            source_text = source_file.read()
    except:
        source_text = None

    # include our source code...
    ourfile = __file__
    if ourfile.endswith('.pyc'):
        ourfile = ourfile[:-1]
    if encoding:
        source = u'# coding=' + encoding.decode('ascii')
    
    with codecs.open(ourfile, 'r', 'ascii') as services_file:
        source = services_file.read()

    main_source = _get_main_source(function)

    source += chr(10) + main_source 

    if source_text is None:
        # we're in a REPL environment, we need to serialize the code...
        #TODO: Remove base64 encoding when json double escape issue is fixed
        source += inspect.getsource(_deserialize_func)
        source += chr(10)
#        source += u'\r\n' #h.kimu
        source += u'__user_function = _deserialize_func(base64.decodestring(' + repr(base64.encodestring(_serialize_func(function)).replace(chr(10), '')) + '), globals())'
    else:
        # we can upload the source code itself...
        source += u'''
# overwrite publish/service with ones which won't re-publish...
import sys
sys.modules['buabuaml'] = buabuaml = type(sys)('buabuaml')
sys.modules['buabuaml.services'] = services = type(sys)('services')
buabuaml.services = services

def publish(func, *args, **kwargs):
    if callable(func):
        return func
    def wrapper(func):
        return func
    return wrapper
services.publish = publish

def service(*args):
    def wrapper(func):
        return func
    return wrapper

def attach(*args, **kwargs):
    def wrapper(func):
        return func
    return wrapper

services.service = service
services.types = types
services.returns = returns
services.attach = attach
services.dataframe_service = attach
services.service_id = attach

'''
        source += source_text
        source += chr(10)
        source += u'__user_function = ' + function.__name__
        source += u'print(__user_function(100,200))'
    
    return source

_known_types = {
    int: {'type':'integer', 'format':'int64'},
    bool: {'type' : 'Boolean'},
    float: {'type': 'number', 'format':'double'},
    str if sys.version_info > (3, ) else unicode: {'type':'string'},
    #complex:'Complex64',
}

OBJECT_NAME = {"type":"string", "format":"string"} # "description":"Python custom serialization"

def _get_annotation(name, func):
    try:
        annotations = func.__annotations__
    except AttributeError:
        return None

    return annotations.get(name)

def _annotation_to_type(annotation):
    if annotation is None:
        return OBJECT_NAME
    
    if isinstance(annotation, str):
        # allow the user to specify the raw string value that will be passed...
        return annotation
    
    return _known_types.get(annotation) or OBJECT_NAME

def _get_arg_type(name, func):
    if name != "return":
        raw_schema = _get_dataframe_schema(func)
        if raw_schema is not None:
            return _annotation_to_type(raw_schema[name])

    annotation = _get_annotation(name, func)
    return _annotation_to_type(annotation)


def _add_file(adding, zip_file):
    
    if isinstance(adding, tuple):
        name, contents = adding
    else:
        name = adding
        contents = None

    if isinstance(name, tuple):
        name, dest_name = name
    else:
        name = dest_name = name
    
    if contents is None:
        contents = file(name, 'rb').read()

    zip_file.writestr(dest_name, contents)
    
def _get_file_name(adding, zip_file):
    
    if isinstance(adding, tuple):
        name, contents = adding
    else:
        name = adding
        contents = None

    if isinstance(name, tuple):
        name, dest_name = name
    else:
        name = dest_name = name
    return dest_name

_DEBUG = True


def _publish_worker(func, workspace_id = None, workspace_token = None, management_endpoint = None, model_uuid = None, model_type = 1, files=()):

    workspace_id = workspace_id
    workspace_token = workspace_token
    management_endpoint = management_endpoint
    script_code = _get_source(func) + chr(10) #chr(10) -> \n
    ret_type = _get_annotation('return', func)

    
    if isinstance(ret_type, tuple):
        # multi-value return
        results = OrderedDict()
        for index, obj_type in enumerate(ret_type):
            results['prediction' + str(index)] = _annotation_to_type(obj_type)
    elif isinstance(ret_type, dict):
        # multi-value return
        results = OrderedDict()
        for name, obj_type in ret_type.items():
            results[name] = _annotation_to_type(obj_type)
    else:
        results = {"prediction": _get_arg_type('return', func)}

    python_version = "python-{}.{}".format(sys.version_info[0],sys.version_info[1])
        
    code_bundle = {
        "InputSchema": {name: _get_arg_type(name, func) for name in _get_args(func)},
        "OutputSchema": results,
        "Language" : python_version,
        "SourceCode": script_code,
    }
    
    attachments = getattr(func, '__attachments__', None)
    file_name = None
    if attachments or files:
        data = BytesIO()
        zip_file = zipfile.PyZipFile(data, 'w')
        #decorator
        if attachments:
            for adding in attachments:
                _add_file(adding, zip_file)
                file_name = _get_file_name(adding, zip_file)
        
        if files:
            for adding in files:
                _add_file(adding, zip_file)
                file_name = _get_file_name(adding, zip_file)
 
        zip_file.close()
        code_bundle['ZipContents'] = base64.b64encode(data.getvalue())

#        f = open('joblib_finalized_model.sav')
#        data_file = f.read();
#        f.close()
#        code_bundle['ZipContents'] = base64.b64encode(data_file)
    
    name = getattr(func, '__service_name__', func.__name__)
    
    service_id = str(getattr(func, '__service_id__', uuid.uuid4())).replace('-', '')

    if model_uuid == None:
        model_uuid = str(getattr(func, '__service_id__', uuid.uuid4())).replace('-', '')
        is_new_model = True
    else:
        model_uuid = model_uuid
        is_new_model = False


    swagger_Url = SWAGGER_URL_FORMAT.format(workspace_id, service_id, 'swagger')
    deploy_url = PUBLISH_URL_FORMAT.format(management_endpoint, 'mli/'+buabuaml.__version__, workspace_id, service_id, 'deploy')
    body = {
        "Name": name,
        "Type": model_type,
        "endpoint": management_endpoint,
        "CodeBundle": code_bundle,
        "Meta":{
            "WorkspaceID" : workspace_id,
            "ServiceID" : service_id,
            "IsNewModel" : is_new_model,
            "ModelUUID" : model_uuid,
            "JWTKey" : workspace_token,
            "Swagger_Url" : swagger_Url,
            "FileName" : file_name,
        }
    }
    
    headers = {'Accept':'application/json','Content-Type':'application/json','Authorization': 'bearer ' + workspace_token}
    resp = requests.post(
        deploy_url, 
        json=body, 
        headers=headers
    )
    '''
    resp = requests.put(
        url, 
        json=body, 
        headers=headers
    )
    '''
    
    if _DEBUG:
        with open(func.__name__ + '.req', 'w') as f:
            f.write(deploy_url + chr(10))
            f.write(json.dumps(body))
            f.close()

        with open(func.__name__ + '.res', 'w') as f:
            f.write(str(resp.status_code) + chr(10))
            f.write(resp.text + chr(10))
            f.close()

    if resp.status_code < 200 or resp.status_code > 299:
        try:
            msg = resp.json()['error']['message']
        except:
            msg = str(resp.status_code)
        raise ValueError('Failed to publish function: ' + msg + chr(10)  + 
                         'Set buabuaml.services._DEBUG = True to enable writing {}.req/{}.res files'.format(func.__name__, func.__name__))


    j = resp.json()
    print (j)
#    epUrl = url + '/endpoints/' + j['DefaultEndpointName']
#    epResp = requests.get(epUrl, headers=headers)
#    endpoints = epResp.json()
#    url = endpoints['ApiLocation'] + '/execute?api-version=2.0'
    return published(swagger_Url, '', '/', func, service_id)
#    return published(url, endpoints['PrimaryKey'], endpoints['HelpLocation'] + '/score', func, service_id)



def publish(func_or_workspace_id, workspace_id_or_token = None, workspace_token_or_none = None, endpoint = None, model_uuid = None, model_type = 1, files=()):

    if not callable(func_or_workspace_id):
        def do_publish(func):
            func.service = _publish_worker(func, func_or_workspace_id, workspace_id_or_token, endpoint,  model_uuid, model_type, files)
            return func
        return do_publish

    return _publish_worker(func_or_workspace_id, workspace_id_or_token, workspace_token_or_none, endpoint,  model_uuid, model_type)

def service(url, api_key, help_url = None):
    '''Marks a function as having been published and causes all invocations to go to the remote
operationalized service.

>>> @service(url, api_key)
>>> def f(a, b):
>>>     pass
'''
    def do_publish(func):
        return published(url, api_key, help_url, func, None)
    return do_publish

def types(**args):
    """Specifies the types used for the arguments of a published service.

@types(a=int, b = str)
def f(a, b):
    pass
"""
    def l(func):
        if hasattr(func, '__annotations__'):
            func.__annotations__.update(args)
        else:
            func.__annotations__ = args
        return func
    return l

def returns(type):
    """Specifies the return type for a published service.

@returns(int)
def f(...):
    pass
"""
    def l(func):
        if hasattr(func, '__annotations__'):
            func.__annotations__['return'] = type
        else:
            func.__annotations__ = {'return': type}
        return func
    return l

def attach(name, contents = None):
    """attaches a file to the payload to be uploaded.

If contents is omitted the file is read from disk.
If name is a tuple it specifies the on-disk filename and the destination filename.
"""
    def do_attach(func):
        if hasattr(func, '__attachments__'):
            func.__attachments__.append((name, contents))
        else:
            func.__attachments__ = [(name, contents)]
        return func
    return do_attach

def service_id(id):
    """Specifies the service ID to enable re-publishing to the same end point.
Can be applied to the function which is being published:

@publish(...)
@service_id('e5dd3903-796f-4544-b7aa-f4e08b2cc639')
def myfunc():
    return 42

When the function is published it will replace any existing instances of the 
function.
"""
    def l(func):
        func.__service_id__ = id
        return func

    return l

def name(name):
    """Provides a friendly name for the published web service which can include spaces and other characters illegal for Python functions.
"""
    def l(func):
        func.__service_name__ = name
        return func

    return l

def dataframe_service(**args):
    """Indicates that the function operations on a data frame.  The function 
    will receive a single input in the form of a data frame, and should return 
    a data frame object.  The schema of the data frame is specified with this 
    decorator.

@publish(...)
@dataframe_service(a = int, b = int)
def myfunc(df):
    return pandas.DataFrame([df['a'][i] + df['b'][i] for i in range(df.shape[0])])
"""
    def l(func):
        func.__dataframe_schema__ = args
        return func

    return l

def input_name(name):
    """specifies the name of the input the web service expects to receive.  Defaults to 'input1'"""
    def l(func):
        func.__input_name__ = name
        return func

    return l    

def output_name(name):
    """specifies the name of the input the web service expects to receive.  Defaults to 'input1'"""
    def l(func):
        func.__output_name__ = name
        return func

    return l    