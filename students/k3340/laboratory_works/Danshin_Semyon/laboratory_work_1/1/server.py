import logging
import socket
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@dataclass
class UPDServer:
    host: str = '0.0.0.0'
    port: int = 8080

    sock: socket.socket = field(init=False)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        logger.info("Server started")

    def serve(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            text_data = data.decode('utf-8')
            logger.info(f"Received data: {text_data}")

            response = b"Hello, client!"

            self.sock.sendto(response, addr)
            logger.info(f"Sent response: {response}")


def main():
    server = UPDServer()
    server.start()
    server.serve()


if __name__ == '__main__':
    main()
