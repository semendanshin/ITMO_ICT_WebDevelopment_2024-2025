import json
import logging
import math
import socket
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@dataclass
class TCPServer:
    host: str = '0.0.0.0'
    port: int = 8080

    sock: socket.socket = field(init=False)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        logger.info("Server started")

    def serve(self, handler: Callable[[bytes], bytes]):
        while True:
            conn, addr = self.sock.accept()

            with conn:
                logger.info(f"Connected by {addr}")

                data = conn.recv(1024)

                response = handler(data)

                conn.sendall(response)
                logger.info(f"Sent response: {response}")


def area_of_parallelogram(a: float, b: float, angle: float) -> float:
    return a * b * math.sin(math.radians(angle))


def handler(data: bytes) -> bytes:
    logger.info(f"Received data: {data}")

    data_json = json.loads(data)

    result = area_of_parallelogram(data_json.get('a'), data_json.get('b'), data_json.get('angle'))

    response = json.dumps({'result': result}).encode('utf-8')

    return response


def main():
    server = TCPServer()
    server.start()
    server.serve(handler)


if __name__ == '__main__':
    main()
