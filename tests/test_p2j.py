import unittest
import pickle
import json
import os
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from safe_pickle_to_json import StrictUnpickler, PermissiveUnpickler
#from safe_pickle_to_json.unpicklers import StrictUnpickler, PermissiveUnpickler, CustomJSONEncoder

# Define test classes at module level
class UnsafeClass:
    def __init__(self):
        self.data = "unsafe"

class TestPickleToJson(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/test_data")
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        # Clean up test files
        for f in self.test_dir.glob("*"):
            f.unlink()
        self.test_dir.rmdir()
        
    def create_pickle(self, data, filename):
        path = self.test_dir / filename
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        return path
        
    def test_strict_basic_types(self):
        data = {
            'string': 'hello',
            'integer': 42,
            'float': 3.14,
            'list': [1, 2, 3],
            'dict': {'a': 1},
            'bool': True,
            'none': None,
            'tuple': (1, 2, 3),
        }
        
        path = self.create_pickle(data, "basic.pickle")
        with open(path, 'rb') as f:
            result = StrictUnpickler(f).load()
        self.assertEqual(result, data)
        
    def test_strict_datetime(self):
        data = {
            'date': date(2024, 3, 14),
            'datetime': datetime(2024, 3, 14, 12, 30),
            'decimal': Decimal('3.14159'),
        }
        
        path = self.create_pickle(data, "datetime.pickle")
        with open(path, 'rb') as f:
            result = StrictUnpickler(f).load()
        self.assertEqual(result, data)
        
    def test_strict_rejects_unsafe(self):
        data = {'unsafe': UnsafeClass()}
        path = self.create_pickle(data, "unsafe.pickle")
        
        with open(path, 'rb') as f:
            with self.assertRaises(pickle.UnpicklingError):
                StrictUnpickler(f).load()
                
    def test_permissive_complex_types(self):
        from collections import OrderedDict, defaultdict
        
        data = {
            'ordered_dict': OrderedDict([('a', 1), ('b', 2)]),
            'default_dict': defaultdict(list, {'key': [1, 2, 3]}),
            'complex_datetime': {
                'date': date(2024, 3, 14),
                'time': datetime.now().time(),
            }
        }
        
        path = self.create_pickle(data, "complex.pickle")
        with open(path, 'rb') as f:
            result = PermissiveUnpickler(f).load()
        
        # Test type equality
        self.assertIsInstance(result['ordered_dict'], OrderedDict)
        self.assertIsInstance(result['default_dict'], defaultdict)
        self.assertEqual(dict(result['ordered_dict']), {'a': 1, 'b': 2})
        
    def test_permissive_rejects_dangerous(self):
        # Create a dangerous pickle that attempts to import os
        dangerous_pickle = (
            b'cos\n'           # Try to import os module
            b'system\n'        # Get system function
            b'(S"echo hacked"\n' # Try to execute command
            b'tR.'            # Execute
        )
        
        path = self.test_dir / "dangerous.pickle"
        with open(path, 'wb') as f:
            f.write(dangerous_pickle)
        
        with open(path, 'rb') as f:
            with self.assertRaises(pickle.UnpicklingError):
                PermissiveUnpickler(f).load()
                
    def test_nested_structures(self):
        data = {
            'nested': {
                'list': [1, {'a': 2}, (3, 4)],
                'dict': {'a': [1, 2], 'b': {'c': 3}},
                'date': date(2024, 3, 14),
            }
        }
        
        path = self.create_pickle(data, "nested.pickle")
        
        # Should work in both modes
        with open(path, 'rb') as f:
            strict_result = StrictUnpickler(f).load()
        with open(path, 'rb') as f:
            permissive_result = PermissiveUnpickler(f).load()
            
        self.assertEqual(strict_result, data)
        self.assertEqual(permissive_result, data)

if __name__ == '__main__':
    unittest.main() 