import sys
from rpc_client import RpcClient
from rpc_server import RpcServer
from student_profile import StudentProfile
from marshalling import validate_types, validate_student_profile, STUDENT_PROFILE_SCHEMA


def run_server():
    print("Starting RPC Server...")
    server = RpcServer()
    server.serve_forever()


def run_client():
    print("=" * 60)
    print("RPC Client Demo - Remote Grade Average Calculation")
    print("=" * 60)

    client = RpcClient()

    profile = StudentProfile(
        name="Ganapathy",
        id=90,
        grades=[23, 45, 78]
    )

    average = client.calculate_grade_average(profile)

    print("=" * 60)
    print(f"Final Result: Grade Average = {average:.2f}")
    print("=" * 60)


def run_validation_tests():
    print("=" * 60)
    print("Testing validate_types() Function")
    print("=" * 60)

    print("\n[Test 1] Valid data - should pass")
    print("-" * 40)
    valid_data = {"name": "John", "id": 123, "grades": [90, 85, 88]}
    try:
        validate_student_profile(valid_data)
        print("Result: PASSED - Data is valid\n")
    except (TypeError, KeyError) as e:
        print(f"Result: FAILED - {e}\n")

    print("[Test 2] String instead of int for 'id' - should raise TypeError")
    print("-" * 40)
    invalid_id = {"name": "John", "id": "123", "grades": [90, 85]}
    try:
        validate_student_profile(invalid_id)
        print("Result: FAILED - Should have raised TypeError\n")
    except TypeError as e:
        print(f"Result: PASSED - Caught TypeError: {e}\n")
    except KeyError as e:
        print(f"Result: FAILED - Wrong exception: {e}\n")

    print("[Test 3] Int instead of string for 'name' - should raise TypeError")
    print("-" * 40)
    invalid_name = {"name": 12345, "id": 123, "grades": [90, 85]}
    try:
        validate_student_profile(invalid_name)
        print("Result: FAILED - Should have raised TypeError\n")
    except TypeError as e:
        print(f"Result: PASSED - Caught TypeError: {e}\n")
    except KeyError as e:
        print(f"Result: FAILED - Wrong exception: {e}\n")

    print("[Test 4] String in grades list - should raise TypeError")
    print("-" * 40)
    invalid_grades = {"name": "John", "id": 123, "grades": [90, "85", 88]}
    try:
        validate_student_profile(invalid_grades)
        print("Result: FAILED - Should have raised TypeError\n")
    except TypeError as e:
        print(f"Result: PASSED - Caught TypeError: {e}\n")
    except KeyError as e:
        print(f"Result: FAILED - Wrong exception: {e}\n")

    print("[Test 5] Missing 'grades' field - should raise KeyError")
    print("-" * 40)
    missing_field = {"name": "John", "id": 123}
    try:
        validate_student_profile(missing_field)
        print("Result: FAILED - Should have raised KeyError\n")
    except KeyError as e:
        print(f"Result: PASSED - Caught KeyError: {e}\n")
    except TypeError as e:
        print(f"Result: FAILED - Wrong exception: {e}\n")

    print("=" * 60)
    print("All validation tests completed!")
    print("=" * 60)


def print_usage():
    print("RPC Framework - Lab DA-1")
    print("-" * 40)
    print("Usage:")
    print("  python main.py server   - Start the RPC server")
    print("  python main.py client   - Run the RPC client")
    print("  python main.py test     - Run type validation tests")
    print()
    print("Or run directly:")
    print("  python rpc_server.py    - Start the server")
    print("  python rpc_client.py    - Run the client")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "server":
            run_server()
        elif sys.argv[1] == "client":
            run_client()
        elif sys.argv[1] == "test":
            run_validation_tests()
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print_usage()
    else:
        print_usage()
