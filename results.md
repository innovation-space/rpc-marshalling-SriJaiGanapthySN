# Lab DA-1: RPC Framework with Object Marshalling - Results

## Submitted by

**Name** Sri Jai Ganapathy S N

**Regno** 22MIC0012

## Objective

Implement a Remote Procedure Call (RPC) framework in Python that supports remote invocation of methods with complex object parameters. Specifically, implement:

```python
float calculate_grade_average(StudentProfile profile)
```

## StudentProfile Object Structure

| Field  | Type         | Description            |
| ------ | ------------ | ---------------------- |
| name   | string       | Student's name         |
| id     | int          | Student's unique ID    |
| grades | list of ints | List of student grades |

## Implementation Details

### 1. Marshalling/Unmarshalling (student_profile.py)

The `StudentProfile` class uses Python's `dataclass` decorator and provides:

- `to_dict()`: Serializes the object to a dictionary (marshalling)
- `from_dict()`: Deserializes a dictionary back to an object (unmarshalling)

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

### 2. RPC Protocol

The framework uses a JSON-based RPC protocol over TCP sockets:

**Request Format:**

```json
{
  "method": "calculate_grade_average",
  "params": {
    "name": "StudentName",
    "id": 123,
    "grades": [85, 90, 78, 92]
  }
}
```

**Response Format:**

```json
{
  "result": 86.25
}
```

**Error Response:**

```json
{
  "error": "Error message"
}
```

### 3. Server Implementation (rpc_server.py)

- Listens on `127.0.0.1:4000`
- Handles incoming RPC requests
- Deserializes `StudentProfile` from JSON (unmarshalling)
- Computes grade average
- Returns result as JSON

### 4. Client Implementation (rpc_client.py)

- Connects to server at `127.0.0.1:4000`
- Serializes `StudentProfile` to JSON (marshalling)
- Sends RPC request
- Receives and parses response

## Test Execution

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

### Server Output (after client connects):

```
[Server] Client connected from ('127.0.0.1', 52345)
[Server] Received request for method: calculate_grade_average
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

### Test Case Details

| Test Input                                    | Expected Output               |
| --------------------------------------------- | ----------------------------- |
| StudentProfile("Ganapathy", 90, [23, 45, 78]) | 48.67 (average of 23, 45, 78) |

**Calculation Verification:**

- Grades: [23, 45, 78]
- Sum: 23 + 45 + 78 = 146
- Count: 3
- Average: 146 / 3 = 48.666... ≈ 48.67 ✓

## Architecture Diagram

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│   RPC Client    │◄───────►│   RPC Server    │
│                 │  TCP    │                 │
│  - StudentProfile        │  - calculate_   │
│    .to_dict()   │  JSON   │    grade_avg() │
│  - call()       │         │  - StudentProfile
│                 │         │    .from_dict() │
└─────────────────┘         └─────────────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│   Marshalling   │         │ Unmarshalling   │
│   (Serialize)   │         │ (Deserialize)   │
│                 │         │                 │
│ StudentProfile  │         │ Dict → Student  │
│   → Dict → JSON │         │   Profile       │
└─────────────────┘         └─────────────────┘
```

## RPC Communication Flow

```
Step 1: Client creates StudentProfile object
        StudentProfile("Ganapathy", 90, [23, 45, 78])
                            │
                            ▼
Step 2: Client marshals object to dictionary
        {"name": "Ganapathy", "id": 90, "grades": [23, 45, 78]}
                            │
                            ▼
Step 3: Client serializes to JSON and sends over TCP
        '{"method": "calculate_grade_average", "params": {...}}'
                            │
                            ▼
Step 4: Server receives and parses JSON
        {"method": "calculate_grade_average", "params": {...}}
                            │
                            ▼
Step 5: Server unmarshals to StudentProfile object
        StudentProfile(name="Ganapathy", id=90, grades=[23,45,78])
                            │
                            ▼
Step 6: Server executes calculate_grade_average()
        sum([23, 45, 78]) / 3 = 48.67
                            │
                            ▼
Step 7: Server sends JSON response
        {"result": 48.666666666666664}
                            │
                            ▼
Step 8: Client receives and displays result
        Grade Average = 48.67
```

## Key Features

1. **Object Marshalling**: Complex objects serialized to JSON for network transport
2. **Socket Communication**: TCP sockets for reliable client-server communication
3. **Error Handling**: Graceful error handling with error messages in responses
4. **Extensible Design**: Easy to add new RPC methods to the handler dictionary
5. **Verbose Logging**: Detailed output showing each step of the RPC process

## Files Structure

```
rpc-marshalling-SriJaiGanapthySN/
├── student_profile.py  # StudentProfile class with marshalling
├── rpc_server.py       # RPC Server implementation
├── rpc_client.py       # RPC Client implementation
├── main.py             # Entry point for server/client
├── results.md          # This results document
└── README.md           # Project documentation
```

## Conclusion

The RPC framework successfully demonstrates:

- Remote procedure invocation over TCP sockets
- Object marshalling/unmarshalling using JSON serialization
- Client-server architecture for distributed computing
- Handling complex data types (custom objects with nested lists)

The `calculate_grade_average` function correctly computes and returns the average of a student's grades when invoked remotely with a `StudentProfile` object.

### Key Learnings

1. **Marshalling** converts complex objects to a format suitable for network transmission (dictionary → JSON)
2. **Unmarshalling** reconstructs objects from received data (JSON → dictionary → object)
3. **RPC abstraction** allows calling remote methods as if they were local functions
4. **TCP sockets** provide reliable, ordered delivery of messages between client and server
