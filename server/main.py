import socket
from core.message import process_message
from common.config import HOST, PORT

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        conn, addr = server.accept()
        with conn:
            print(f"[SERVER] Connection established with {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                print(f"[SERVER] Received: {message}")
                response = process_message(message)
                conn.sendall(response.encode())

            print(f"[SERVER] Connection with {addr} closed.")

if __name__ == "__main__":
    run_server()
