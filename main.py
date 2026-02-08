

import sys
from rpc_client import RpcClient
from rpc_server import RpcServer
from student_profile import StudentProfile


def run_server():
    """Start the RPC server."""
    print("Starting RPC Server...")
    server = RpcServer()
    server.serve_forever()


def run_client():
    """Run the RPC client demo with a sample StudentProfile."""
    print("=" * 60)
    print("RPC Client Demo - Remote Grade Average Calculation")
    print("=" * 60)
    
    client = RpcClient()
    
    # Create a StudentProfile object
    profile = StudentProfile(
        name="Ganapathy",
        id=90,
        grades=[23, 45, 78]
    )
    
    # Call the remote method
    average = client.calculate_grade_average(profile)
    
    print("=" * 60)
    print(f"Final Result: Grade Average = {average:.2f}")
    print("=" * 60)


def print_usage():
    """Print usage instructions."""
    print("RPC Framework - Lab DA-1")
    print("-" * 40)
    print("Usage:")
    print("  python main.py server   - Start the RPC server")
    print("  python main.py client   - Run the RPC client")
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
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print_usage()
    else:
        print_usage()
