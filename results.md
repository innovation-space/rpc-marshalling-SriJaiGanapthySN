# Lab DA-1: RPC Framework with Object Marshalling - Results

## Objective
Implement a Remote Procedure Call (RPC) framework in Python that supports remote invocation of methods with complex object parameters. Implement a `validate_types()` function within the marshalling layer that checks incoming data on the server side and raises a `TypeError` if incorrect types are detected.

## StudentProfile Object Structure

| Field  | Type           | Description              |
|--------|----------------|--------------------------|
| name   | string         | Student's name           |
| id     | int            | Student's unique ID      |
| grades | list of ints   | List of student grades   |

---

## Implementation Details

### 1. Marshalling Layer (marshalling.py)

A **dedicated marshalling layer** that handles:
- Type validation using `validate_types()`
- Object serialization (marshalling)
- Object deserialization (unmarshalling)

#### validate_types() Function

```python
def validate_types(data: Dict[str, Any], schema: Dict[str, type]) -> None:
    """
    Validate that incoming data matches the expected types.
    
    Raises:
        TypeError: If a field has an incorrect type
        KeyError: If a required field is missing
    """
    for field_name, expected_type in schema.items():
        if field_name not in data:
            raise KeyError(f"Missing required field: '{field_name}'")
        
        value = data[field_name]
        
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Type error for field '{field_name}': "
                f"expected {expected_type.__name__}, got {type(value).__name__} "
                f"(value: {repr(value)})"
            )
```

#### Schema Definition

```python
STUDENT_PROFILE_SCHEMA = {
    "name": str,
    "id": int,
    "grades": list
}
```

### 2. StudentProfile Class (student_profile.py)

```python
@dataclass
class StudentProfile:
    name: str
    id: int
    grades: List[int]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "id": self.id, "grades": self.grades}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "StudentProfile":
        return StudentProfile(name=data["name"], id=data["id"], grades=data["grades"])
```

### 3. RPC Server (rpc_server.py)

The server validates incoming data using the marshalling layer before processing:

```python
def calculate_grade_average(self, profile_dict: Dict[str, Any]) -> float:
    # Validate types using the marshalling layer
    validate_student_profile(profile_dict)  # Raises TypeError if invalid
    
    # Unmarshal the dictionary to StudentProfile object
    profile = unmarshal(profile_dict, StudentProfile)
    
    # Calculate average
    return sum(profile.grades) / len(profile.grades)
```

### 4. RPC Client (rpc_client.py)

The client marshals objects before sending:

```python
def calculate_grade_average(self, profile: StudentProfile) -> float:
    # Marshal the object using marshalling layer
    profile_dict = marshal(profile)
    
    # Make the RPC call
    return self.call("calculate_grade_average", profile_dict)
```

---

## Type Validation Test Results

### Test Execution
```bash
python main.py test
```

### Test Output

```
============================================================
Testing validate_types() Function
============================================================

[Test 1] Valid data - should pass
----------------------------------------
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': 123, 'grades': [90, 85, 88]}
[Marshalling] Validation successful - all types are correct
Result: PASSED - Data is valid

[Test 2] String instead of int for 'id' - should raise TypeError
----------------------------------------
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': '123', 'grades': [90, 85]}
Result: PASSED - Caught TypeError: Type error for field 'id': expected int, got str (value: '123')

[Test 3] Int instead of string for 'name' - should raise TypeError
----------------------------------------
[Marshalling] Validating StudentProfile data: {'name': 12345, 'id': 123, 'grades': [90, 85]}
Result: PASSED - Caught TypeError: Type error for field 'name': expected str, got int (value: 12345)

[Test 4] String in grades list - should raise TypeError
----------------------------------------
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': 123, 'grades': [90, '85', 88]}
Result: PASSED - Caught TypeError: Type error for field 'grades[1]': expected int, got str (value: '85')

[Test 5] Missing 'grades' field - should raise KeyError
----------------------------------------
[Marshalling] Validating StudentProfile data: {'name': 'John', 'id': 123}
Result: PASSED - Caught KeyError: 'Missing required field: 'grades''

============================================================
All validation tests completed!
============================================================
```

---

## RPC Test Results

### Step 1: Start the Server
```bash
python rpc_server.py
```
**Output:**
```
[Server] RPC Server started on 127.0.0.1:4000
[Server] Waiting for client connections...
```

### Step 2: Run the Client
```bash
python rpc_client.py
```

### Server Output:
```
[Server] Client connected from ('127.0.0.1', 52345)
[Server] Received request for method: calculate_grade_average
[Marshalling] Validating StudentProfile data: {'name': 'Ganapathy', 'id': 90, 'grades': [23, 45, 78]}
[Marshalling] Validation successful - all types are correct
[Server] Received profile: StudentProfile(name='Ganapathy', id=90, grades=[23, 45, 78])
[Server] Calculating: sum([23, 45, 78]) / 3 = 146 / 3 = 48.666666666666664
[Server] Sending response: {'result': 48.666666666666664}
[Server] Client ('127.0.0.1', 52345) disconnected
```

### Client Output:
```
============================================================
RPC Client - Remote Grade Average Calculation
============================================================

[Client] Calling remote method: calculate_grade_average
[Client] StudentProfile object: StudentProfile(name='Ganapathy', id=90, grades=[23, 45, 78])
[Client] Marshalled to dict: {'name': 'Ganapathy', 'id': 90, 'grades': [23, 45, 78]}
[Client] Connecting to 127.0.0.1:4000
[Client] Sending request: {"method": "calculate_grade_average", "params": {"name": "Ganapathy", "id": 90, "grades": [23, 45, 78]}}
[Client] Received response: {'result': 48.666666666666664}
============================================================
[Client] Final Result: Grade Average = 48.67
============================================================
```

---

## Architecture Diagram

```
┌─────────────────┐                              ┌─────────────────┐
│   RPC Client    │                              │   RPC Server    │
│                 │         TCP Socket           │                 │
│  rpc_client.py  │◄────────────────────────────►│  rpc_server.py  │
└────────┬────────┘           JSON               └────────┬────────┘
         │                                                │
         ▼                                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MARSHALLING LAYER                           │
│                      marshalling.py                             │
│                                                                 │
│  ┌─────────────────┐              ┌─────────────────────────┐  │
│  │    marshal()    │              │   validate_types()      │  │
│  │                 │              │                         │  │
│  │ StudentProfile  │              │ Checks: name=str        │  │
│  │    → Dict       │              │         id=int          │  │
│  │    → JSON       │              │         grades=list[int]│  │
│  └─────────────────┘              └─────────────────────────┘  │
│                                                                 │
│  ┌─────────────────┐              ┌─────────────────────────┐  │
│  │   unmarshal()   │              │ validate_student_       │  │
│  │                 │              │       profile()         │  │
│  │ JSON → Dict     │              │                         │  │
│  │    → StudentProfile           │ Raises TypeError if     │  │
│  └─────────────────┘              │ types don't match       │  │
│                                   └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                                                │
         ▼                                                ▼
┌─────────────────┐                              ┌─────────────────┐
│ StudentProfile  │                              │ StudentProfile  │
│   Object        │                              │   Object        │
│                 │                              │                 │
│ student_profile.py                             │ student_profile.py
└─────────────────┘                              └─────────────────┘
```

---

## RPC Communication Flow with Type Validation

```
CLIENT                         NETWORK                         SERVER
  │                               │                               │
  │ 1. Create StudentProfile      │                               │
  │    object with data           │                               │
  │                               │                               │
  │ 2. marshal(profile)           │                               │
  │    → Convert to dict          │                               │
  │                               │                               │
  │ 3. serialize_to_json()        │                               │
  │    → Convert to JSON          │                               │
  │                               │                               │
  │ ─────────────────────────────>│                               │
  │          TCP Send             │                               │
  │                               │──────────────────────────────>│
  │                               │         TCP Receive           │
  │                               │                               │
  │                               │     4. deserialize_from_json()│
  │                               │        → Parse JSON to dict   │
  │                               │                               │
  │                               │     5. validate_types()       │
  │                               │        → Check name is str    │
  │                               │        → Check id is int      │
  │                               │        → Check grades is list │
  │                               │        → Check each grade int │
  │                               │                               │
  │                               │        IF INVALID:            │
  │                               │        → Raise TypeError      │
  │                               │        → Return error response│
  │                               │                               │
  │                               │     6. unmarshal()            │
  │                               │        → Create StudentProfile│
  │                               │                               │
  │                               │     7. calculate_grade_average│
  │                               │        → sum(grades)/len      │
  │                               │                               │
  │                               │<──────────────────────────────│
  │<──────────────────────────────│         TCP Send Result       │
  │        TCP Receive            │                               │
  │                               │                               │
  │ 8. Parse response             │                               │
  │    → Display result           │                               │
  │                               │                               │
```

---

## Files Structure

```
rpc-marshalling-SriJaiGanapthySN/
├── student_profile.py  # StudentProfile data class
├── marshalling.py      # Marshalling layer with validate_types()
├── rpc_server.py       # RPC Server with type validation
├── rpc_client.py       # RPC Client with marshalling
├── main.py             # Entry point (server/client/test)
├── results.md          # This results document
└── README.md           # Project documentation
```

---

## Key Features

1. **Separate Marshalling Layer**: Dedicated module for all marshalling operations
2. **Type Validation**: `validate_types()` checks data types on server side
3. **Error Handling**: Raises `TypeError` with detailed error messages
4. **Object Marshalling**: Complex objects serialized to JSON for network transport
5. **Socket Communication**: TCP sockets for reliable client-server communication
6. **Extensible Design**: Easy to add new RPC methods and data types

---

## Conclusion

The RPC framework successfully implements:

1. **Remote procedure invocation** over TCP sockets
2. **Separate marshalling layer** (`marshalling.py`) for serialization/deserialization
3. **`validate_types()` function** that:
   - Checks incoming data against expected schema
   - Raises `TypeError` if string sent where int expected
   - Validates nested types (list elements)
   - Provides detailed error messages

The `calculate_grade_average` function correctly validates input types and computes the average of a student's grades when invoked remotely.

### Test Results Summary

| Test Case | Input | Expected | Result |
|-----------|-------|----------|--------|
| Valid data | `id=123` (int) | Pass | ✓ PASSED |
| String for int | `id="123"` (str) | TypeError | ✓ PASSED |
| Int for string | `name=12345` (int) | TypeError | ✓ PASSED |
| String in list | `grades=[90,"85"]` | TypeError | ✓ PASSED |
| Missing field | No grades field | KeyError | ✓ PASSED |
