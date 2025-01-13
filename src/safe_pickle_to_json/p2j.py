import json
import argparse
import pickle
from .unpicklers import StrictUnpickler, PermissiveUnpickler, CustomJSONEncoder

def get_args():
    parser = argparse.ArgumentParser(description='Convert pickle file to json')
    parser.add_argument('input', help='Input pickle file path')
    parser.add_argument('output', nargs='?', help='Output json file path (optional, defaults to input_name.json)')
    parser.add_argument('--permissive', action='store_true', help='Use less strict (blacklist-based) unpickling')
    args = parser.parse_args()
    
    if args.output is None:
        args.output = args.input.rsplit('.', 1)[0] + '.json'
    
    return args

def main():
    try:
        args = get_args()
        print(f"Converting {args.input} to {args.output}")
        
        UnpicklerClass = PermissiveUnpickler if args.permissive else StrictUnpickler
        
        with open(args.input, 'rb') as f:
            data = UnpicklerClass(f).load()
        
        with open(args.output, 'w') as fs:
            json.dump(data, fs, cls=CustomJSONEncoder, indent=4)
        
        print(f"Successfully converted pickle to JSON: {args.output}")
        return 0
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        return 1
    except pickle.UnpicklingError as e:
        print(f"Error: Invalid or unsafe pickle file - {e}")
        return 1
    except json.JSONEncodeError as e:
        print(f"Error: Failed to encode data to JSON - {e}")
        return 1
    except Exception as e:
        print(f"Error: Unexpected error occurred - {e}")
        return 1

if __name__ == "__main__":
    main()