import json
import logging
import socket
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@dataclass
class TCPClient:
    host: str = '0.0.0.0'
    port: int = 8080

    def send(self, data: bytes) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(data)

            response = sock.recv(1024)

        return response

def area_of_parallelogram(a: float, b: float, angle: float) -> float:
    payload = json.dumps({'a': a, 'b': b, 'angle': angle}).encode('utf-8')
    client = TCPClient()
    response = client.send(payload)
    response_json = json.loads(response)
    return response_json.get('result')

def main():
    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    angle = float(input("Enter angle: "))

    result = area_of_parallelogram(a, b, angle)

    print(f"Result: {result}")


if __name__ == '__main__':
    main()
