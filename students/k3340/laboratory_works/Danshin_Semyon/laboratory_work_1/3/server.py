"""
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.
"""

import socket
import logging
from dataclasses import dataclass
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

    def start(self, handler: Callable[[bytes], bytes]):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(1)

            logger.info(f"Server started on {self.host}:{self.port}")

            while True:
                conn, addr = sock.accept()
                with conn:
                    logger.info(f"Connection from {addr}")

                    data = conn.recv(1024)
                    response = handler(data)
                    conn.sendall(response)

def handler(_: bytes) -> bytes:
    response_template = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n{}\n"

    with open("index.html", "r") as file:
        response = file.read()

    return response_template.format(response).encode('utf-8')

def main():
    server = TCPServer(host="localhost")
    server.start(handler)

if __name__ == '__main__':
    main()
