#!/bin/python3
import builtins
import io
import json
import pickle
from datetime import datetime, date, time, timedelta
from decimal import Decimal
import sys

class StrictUnpickler:
    def __init__(self, file):
        self._file = file

    def load(self):
        safe_ops = {
            # Basic data structure construction
            (b'c__builtin__\ndict\n', 'dict'),
            (b'c__builtin__\nlist\n', 'list'),
            (b'c__builtin__\ntuple\n', 'tuple'),
            (b'c__builtin__\nstr\n', 'str'),
            (b'c__builtin__\nint\n', 'int'),
            (b'c__builtin__\nfloat\n', 'float'),
            (b'c__builtin__\nbool\n', 'bool'),
            # Date and time objects
            (b'cdatetime\ndate\n', 'date'),
            (b'cdatetime\ndatetime\n', 'datetime'),
            (b'cdatetime\ntime\n', 'time'),
            (b'cdatetime\ntimedelta\n', 'timedelta'),
            # Decimal for precise numbers
            (b'cdecimal\nDecimal\n', 'Decimal'),
            # Basic collections
            (b'c__builtin__\nset\n', 'set'),
            (b'c__builtin__\nfrozenset\n', 'frozenset'),
            # Basic pickle operations
            (b'(', 'MARK'),
            (b'.', 'STOP'),
            (b'N', 'NONE'),
            (b'I', 'INT'),
            (b'F', 'FLOAT'),
            (b'S', 'STRING'),
            (b'V', 'UNICODE'),
            (b'}', 'DICT'),
            (b']', 'LIST'),
            (b')', 'TUPLE'),
        }

        unpickler = pickle._Unpickler(self._file)
        
        def _safe_find_class(module, name):
            op = (f'c{module}\n{name}\n'.encode('ascii'), name)
            if op not in safe_ops:
                raise pickle.UnpicklingError(f"Unsafe operation: {module}.{name}")
            
            if module == "builtins":
                if name in {'dict', 'list', 'tuple', 'str', 'int', 'float', 'bool', 'set', 'frozenset'}:
                    return getattr(builtins, name)
            elif module == "datetime":
                if name in {'date', 'datetime', 'time', 'timedelta'}:
                    import datetime
                    return getattr(datetime, name)
            elif module == "decimal" and name == "Decimal":
                return Decimal
                
            raise pickle.UnpicklingError(f"Unsafe operation: {module}.{name}")

        unpickler.find_class = _safe_find_class
        return unpickler.load()

class PermissiveUnpickler:
    def __init__(self, file):
        self._file = file

    def load(self):
        dangerous_modules = {
            'subprocess', 'os', 'sys', 'base64',
            'pickle', 'marshal', 'code', 'codecs',
            'multiprocessing', 'threading', 'socket',
            'posix', 'nt', 'pathlib', 'tempfile',
            'shutil', 'importlib', '_imp', 'typing',
            'types', 'functools', 'gc', 'copyreg',
            'io', 'pty', 'platform', 'tokenize',
            'linecache', 'trace', 'ast', 'cmd',
            'compileall', 'dis', 'pickletools',
        }

        dangerous_names = {
            # Function/code execution
            'eval', 'exec', 'compile', 'globals', 'locals',
            'getattr', 'setattr', 'delattr', 'hasattr',
            '__import__', '__builtins__', '__main__',
            # File operations
            'open', 'read', 'write', 'file',
            # Object/class manipulation
            'type', 'object', 'property', 'classmethod',
            'staticmethod', '__new__', '__init__', '__del__',
            '__getattribute__', '__setattr__', '__delattr__',
            '__class__', '__bases__', '__mro__', '__subclasses__',
            # System operations
            'system', 'popen', 'spawn', 'fork', 'exec',
            # Module operations
            'import', 'reload', '__loader__', '__spec__',
        }

        unpickler = pickle._Unpickler(self._file)
        
        def _find_class(module, name):
            # Special handling for builtins
            if module == 'builtins':
                if name in {'dict', 'list', 'tuple', 'set', 'frozenset', 
                          'str', 'int', 'float', 'bool', 'type'}:
                    return getattr(builtins, name)
                if name in dangerous_names:
                    raise pickle.UnpicklingError(
                        f"Security: blocked access to dangerous name {name}"
                    )
            
            # Block dangerous modules
            if module in dangerous_modules:
                raise pickle.UnpicklingError(
                    f"Security: blocked access to dangerous module {module}"
                )
            
            # Block dangerous names regardless of module
            if name in dangerous_names:
                raise pickle.UnpicklingError(
                    f"Security: blocked access to dangerous name {name}"
                )
            
            # Allow safe modules
            try:
                __import__(module)
                mod = sys.modules[module]
                return getattr(mod, name)
            except Exception as e:
                raise pickle.UnpicklingError(
                    f"Security: failed to load {module}.{name}: {str(e)}"
                )

        unpickler.find_class = _find_class
        return unpickler.load()

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        return super().default(obj)