import json
import logging
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.data = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def run(self):
        logger.info(f"Server started on {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            with conn:
                logger.info(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode("utf-8")
                logger.info(f"Received data: {data}")

                response = self.handle_request(data)

                conn.sendall(self.format_response(200, response).encode("utf-8"))

    @staticmethod
    def format_response(code: int, data: str) -> str:
        return f"HTTP/1.1 {code}\n\n{data}"

    def handle_request(self, data: str) -> str:
        lines = data.split("\n")
        method, path, protocol = lines[0].split(" ")

        body = data.split("\r\n\r\n")[-1]

        if method == "GET":
            return self.get_data()

        if method == "POST":
            self.save_data(body)
            return "Data saved"

        return "Unknown command"

    def save_data(self, data: str):
        data = json.loads(data)
        self.data.append(data)
        logger.info(f"Data saved: {data}")

    def get_data(self) -> str:
        return json.dumps(self.data)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080

    server = Server(host, port)

    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        sys.exit(0)
