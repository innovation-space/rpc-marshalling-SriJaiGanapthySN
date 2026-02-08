[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/PlHljgVi)

# Lab DA-1: RPC Framework with Object Marshalling

## Overview

A Python-based Remote Procedure Call (RPC) framework that supports marshalling/unmarshalling of complex objects for remote method invocation.

## Features

- Remote invocation of `calculate_grade_average(StudentProfile profile)`
- JSON-based serialization for object marshalling
- TCP socket communication between client and server
- Support for complex data types (StudentProfile with nested list)

## StudentProfile Object

```python
@dataclass
class StudentProfile:
    name: str          # Student's name
    id: int            # Student's unique ID
    grades: List[int]  # List of grades
```

## Files

| File                 | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `student_profile.py` | StudentProfile class with marshalling/unmarshalling methods |
| `rpc_server.py`      | RPC Server implementation with calculate_grade_average      |
| `rpc_client.py`      | RPC Client implementation for remote procedure calls        |
| `main.py`            | Entry point for running server/client                       |
| `results.md`         | Detailed results and documentation                          |

## How to Run

### Start the Server

```bash
python rpc_server.py
```

### Run the Client (in another terminal)

```bash
python rpc_client.py
```

### Or use main.py

```bash
python main.py server   # Start server
python main.py client   # Run client
```

## Example Output

### Server Terminal

```
[Server] RPC Server started on 127.0.0.1:4000
[Server] Waiting for client connections...

[Server] Client connected from ('127.0.0.1', 52345)
[Server] Received request for method: calculate_grade_average
[Server] Received profile: StudentProfile(name='Ganapathy', id=90, grades=[23, 45, 78])
[Server] Calculating: sum([23, 45, 78]) / 3 = 146 / 3 = 48.666666666666664
[Server] Sending response: {'result': 48.666666666666664}
```

### Client Terminal

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
