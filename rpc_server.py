import json
import socket
from typing import Dict, Any

from student_profile import StudentProfile
from marshalling import validate_student_profile, unmarshal


class RpcServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 4000):
        self.host = host
        self.port = port
        self.handlers = {
            "calculate_grade_average": self.calculate_grade_average
        }

    def calculate_grade_average(self, profile_dict: Dict[str, Any]) -> float:
        validate_student_profile(profile_dict)

        profile = unmarshal(profile_dict, StudentProfile)
        print(f"[Server] Received profile: {profile}")

        if not profile.grades:
            print("[Server] No grades found, returning 0.0")
            return 0.0

        total = sum(profile.grades)
        count = len(profile.grades)
        average = total / count

        print(f"[Server] Calculating: sum({profile.grades}) / {count} = {total} / {count} = {average}")
        return average

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params")

        print(f"[Server] Received request for method: {method}")

        if method not in self.handlers:
            return {"error": f"Unknown method: {method}"}

        try:
            result = self.handlers[method](params)
            return {"result": result}
        except TypeError as e:
            print(f"[Server] Type validation failed: {e}")
            return {"error": f"TypeError: {str(e)}"}
        except KeyError as e:
            print(f"[Server] Missing field: {e}")
            return {"error": f"KeyError: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[Server] RPC Server started on {self.host}:{self.port}")
            print("[Server] Waiting for client connections...")

            while True:
                conn, addr = server_socket.accept()
                print(f"\n[Server] Client connected from {addr}")

                with conn:
                    data = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                        if b"\n" in data:
                            line, _, rest = data.partition(b"\n")
                            data = rest
                            request = json.loads(line.decode("utf-8"))
                            response = self.handle_request(request)
                            print(f"[Server] Sending response: {response}")
                            conn.sendall((json.dumps(response) + "\n").encode("utf-8"))

                print(f"[Server] Client {addr} disconnected")


if __name__ == "__main__":
    server = RpcServer()
    server.serve_forever()
