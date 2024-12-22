import logging
import socket
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@dataclass
class UDPClient:
    host: str = '0.0.0.0'
    port: int = 8080

    def send(self, data: bytes) -> bytes:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.host, self.port))

        response, _ = sock.recvfrom(1024)

        return response

def main():
    client = UDPClient()
    logger.debug("Client started")
    response = client.send(b'Hello, server!')
    logger.info(f"Received response: {response}")


if __name__ == '__main__':
    main()
