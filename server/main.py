import socket
import threading
from core.message import process_message
from common.config import HOST, PORT

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr[0]}:{addr[1]}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"[SERVER] From {addr[0]}:{addr[1]}: {message}")
            response = process_message(message)
            conn.sendall(response.encode())
    finally:
        print(f"[SERVER] Connection closed from {addr[0]}:{addr[1]}")
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down gracefully...")
