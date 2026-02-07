from client import RpcClient
from common import StudentProfile
from server import RpcServer


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] == "server":
        server = RpcServer()
        server.serve_forever()
    elif len(sys.argv) >= 2 and sys.argv[1] == "client":
        client = RpcClient()
        profile = StudentProfile("Ganapathy", 90, [23, 45, 78])
        avg = client.call("calculate_grade_average", profile.to_dict())
        print("Remote average:", avg)
    else:
        print("Usage:")
        print("  python server.py")
        print("  python client.py")