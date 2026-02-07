import json
import socket
from typing import Dict, Any

from common import StudentProfile


class RpcServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 4000):
        self.host = host
        self.port = port
        self.handlers = {
            "calculate_grade_average": self.calculate_grade_average
        }

    def calculate_grade_average(self, profile_dict: Dict[str, Any]) -> float:
        profile = StudentProfile.from_dict(profile_dict)
        if not profile.grades:
            return 0.0
        return sum(profile.grades) / len(profile.grades)

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params")

        if method not in self.handlers:
            return {"error": f"Unknown method: {method}"}

        try:
            result = self.handlers[method](params)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[Server] Listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
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
                            conn.sendall((json.dumps(response) + "\n").encode("utf-8"))


if __name__ == "__main__":
    server = RpcServer()
    server.serve_forever()
