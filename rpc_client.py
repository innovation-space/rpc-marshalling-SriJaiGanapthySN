import json
import socket
from typing import Dict, Any

from student_profile import StudentProfile
from marshalling import marshal


class RpcClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 4000):
        self.host = host
        self.port = port

    def call(self, method: str, params: Dict[str, Any]) -> Any:
        request = {"method": method, "params": params}

        print(f"[Client] Connecting to {self.host}:{self.port}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))

            request_json = json.dumps(request)
            print(f"[Client] Sending request: {request_json}")
            sock.sendall((request_json + "\n").encode("utf-8"))

            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b"\n" in response_data:
                    line, _, _ = response_data.partition(b"\n")
                    response = json.loads(line.decode("utf-8"))
                    print(f"[Client] Received response: {response}")

                    if "error" in response:
                        raise RuntimeError(response["error"])
                    return response["result"]

    def calculate_grade_average(self, profile: StudentProfile) -> float:
        print(f"\n[Client] Calling remote method: calculate_grade_average")
        print(f"[Client] StudentProfile object: {profile}")

        profile_dict = marshal(profile)
        print(f"[Client] Marshalled to dict: {profile_dict}")

        result = self.call("calculate_grade_average", profile_dict)

        return result


if __name__ == "__main__":
    client = RpcClient()

    profile = StudentProfile(
        name="Ganapathy",
        id=90,
        grades=[23, 45, 78]
    )

    print("=" * 60)
    print("RPC Client - Remote Grade Average Calculation")
    print("=" * 60)

    average = client.calculate_grade_average(profile)

    print("=" * 60)
    print(f"[Client] Final Result: Grade Average = {average:.2f}")
    print("=" * 60)
