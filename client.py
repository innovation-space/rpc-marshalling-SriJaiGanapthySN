import json
import socket
from typing import Dict, Any

from common import StudentProfile


class RpcClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 4000):
        self.host = host
        self.port = port

    def call(self, method: str, params: Dict[str, Any]) -> Any:
        request = {"method": method, "params": params}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall((json.dumps(request) + "\n").encode("utf-8"))
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b"\n" in response_data:
                    line, _, _ = response_data.partition(b"\n")
                    response = json.loads(line.decode("utf-8"))
                    if "error" in response:
                        raise RuntimeError(response["error"])
                    return response["result"]


if __name__ == "__main__":
    client = RpcClient()
    profile = StudentProfile("Ganapathy", 90, [23, 45, 78])
    avg = client.call("calculate_grade_average", profile.to_dict())
    print("Remote average:", avg)
