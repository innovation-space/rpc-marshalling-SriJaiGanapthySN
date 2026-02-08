"""
RPC Client Implementation

This module implements a TCP-based RPC client that can invoke remote procedures.
It handles object marshalling (serialization) before sending requests.
"""

import json
import socket
from typing import Dict, Any

from student_profile import StudentProfile


class RpcClient:
    """
    RPC Client that connects to the server and invokes remote methods.
    
    The client serializes method calls to JSON and sends them over TCP.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 4000):
        """
        Initialize the RPC Client.
        
        Args:
            host: Server IP address (default: localhost)
            port: Server port number (default: 4000)
        """
        self.host = host
        self.port = port

    def call(self, method: str, params: Dict[str, Any]) -> Any:
        """
        Invoke a remote procedure on the server.
        
        Args:
            method: Name of the remote method to call
            params: Parameters to pass to the method (as dictionary)
            
        Returns:
            The result returned by the server
            
        Raises:
            RuntimeError: If the server returns an error
        """
        request = {"method": method, "params": params}
        
        print(f"[Client] Connecting to {self.host}:{self.port}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            
            # Send the request
            request_json = json.dumps(request)
            print(f"[Client] Sending request: {request_json}")
            sock.sendall((request_json + "\n").encode("utf-8"))
            
            # Receive the response
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
        """
        Convenience method to calculate grade average remotely.
        
        This method handles the marshalling of StudentProfile automatically.
        
        Args:
            profile: StudentProfile object to send to the server
            
        Returns:
            The calculated average grade
        """
        print(f"\n[Client] Calling remote method: calculate_grade_average")
        print(f"[Client] StudentProfile object: {profile}")
        
        # Marshal the object to dictionary
        profile_dict = profile.to_dict()
        print(f"[Client] Marshalled to dict: {profile_dict}")
        
        # Make the RPC call
        result = self.call("calculate_grade_average", profile_dict)
        
        return result


if __name__ == "__main__":
    # Create client
    client = RpcClient()
    
    # Create a StudentProfile object
    profile = StudentProfile(
        name="Ganapathy",
        id=90,
        grades=[23, 45, 78]
    )
    
    print("=" * 60)
    print("RPC Client - Remote Grade Average Calculation")
    print("=" * 60)
    
    # Call the remote method
    average = client.calculate_grade_average(profile)
    
    print("=" * 60)
    print(f"[Client] Final Result: Grade Average = {average:.2f}")
    print("=" * 60)
