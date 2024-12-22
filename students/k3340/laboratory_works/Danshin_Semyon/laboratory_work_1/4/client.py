import socket
import threading

def listen_for_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    sock.close()

def main():
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

    while True:
        message = input("")
        if message.lower() == 'exit':
            break
        sock.sendall(message.encode('utf-8'))

    sock.close()

if __name__ == '__main__':
    main()