import logging
import socket
import threading
from collections.abc import Callable
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@dataclass
class TCPServer:
    host: str = '127.0.0.1'
    port: int = 8080

    running: bool = field(default=False, init=False)

    def start(self, handler: Callable[[socket.socket], None]):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        logger.info(f"Server started on {self.host}:{self.port}")

        self.running = True

        while self.running:
            conn, addr = sock.accept()
            logger.info(f"Connection from {addr}")

            threading.Thread(target=handler, args=(conn,), daemon=True).start()

    def stop(self):
        self.running = False


@dataclass
class ChatServer:
    server: TCPServer
    users: dict[socket.socket, str] = field(default_factory=dict, init=False)

    def handler(self, conn: socket.socket):
        # Register the user
        conn.sendall(b"Enter your username: ")
        username = conn.recv(1024).decode('utf-8').strip()
        self.users[conn] = username
        logger.info(f"User {username} connected")

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8').strip()
                logger.info(f"Message from {username}: {message}")

                for client in self.users:
                    if client == conn:
                        continue
                    client.sendall(f"{username}: {message}".encode('utf-8'))
        finally:
            conn.close()
            del self.users[conn]
            logger.info(f"User {username} disconnected")

    def start(self):
        self.server.start(self.handler)


def main():
    server = TCPServer()
    chat_server = ChatServer(server)

    chat_server.start()


if __name__ == '__main__':
    main()
