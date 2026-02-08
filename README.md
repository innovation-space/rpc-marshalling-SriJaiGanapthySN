[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/PlHljgVi)

# Lab DA-1: RPC Framework with Object Marshalling

## Overview
A Python-based Remote Procedure Call (RPC) framework that supports marshalling/unmarshalling of complex objects for remote method invocation. Includes a dedicated marshalling layer with type validation.

## Features
- Remote invocation of `calculate_grade_average(StudentProfile profile)`
- **Separate marshalling layer** with `validate_types()` function
- JSON-based serialization for object marshalling
- TCP socket communication between client and server
- **Type validation** - raises `TypeError` for incorrect data types

## StudentProfile Object
```python
@dataclass
class StudentProfile:
    name: str          # Student's name (string)
    id: int            # Student's unique ID (integer)
    grades: List[int]  # List of grades (list of integers)
```

## Files
| File | Description |
|------|-------------|
| `student_profile.py` | StudentProfile data class |
| `marshalling.py` | **Marshalling layer** with `validate_types()` function |
| `rpc_server.py` | RPC Server with type validation |
| `rpc_client.py` | RPC Client for remote procedure calls |
| `main.py` | Entry point for server/client/tests |
| `results.md` | Detailed results and documentation |

## Marshalling Layer (`marshalling.py`)

The marshalling layer provides:
- `validate_types(data, schema)` - Validates data types against a schema
- `validate_student_profile(data)` - Validates StudentProfile data
- `marshal(obj)` - Converts object to dictionary
- `unmarshal(data, class)` - Converts dictionary to object

### Type Validation Example
```python
from marshalling import validate_student_profile

# Valid data - passes validation
valid_data = {"name": "John", "id": 123, "grades": [90, 85]}
validate_student_profile(valid_data)  # OK

# Invalid data - raises TypeError
invalid_data = {"name": "John", "id": "123", "grades": [90, 85]}  # id is string!
validate_student_profile(invalid_data)  # Raises TypeError
```

## How to Run

### Start the Server
```bash
python rpc_server.py
```

### Run the Client (in another terminal)
```bash
python rpc_client.py
```

### Run Type Validation Tests
```bash
python main.py test
```

### Using main.py
```bash
python main.py server   # Start server
python main.py client   # Run client
python main.py test     # Run validation tests
```

## Example Output

### Type Validation Test Output
```
============================================================
Testing validate_types() Function
============================================================

[Test 1] Valid data - should pass
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': 123, 'grades': [90, 85, 88]}
[Marshalling] Validation successful - all types are correct
Result: PASSED - Data is valid

[Test 2] String instead of int for 'id' - should raise TypeError
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': '123', 'grades': [90, 85]}
Result: PASSED - Caught TypeError: Type error for field 'id': expected int, got str (value: '123')
```

## Author
Sri Jai Ganapthy SN
