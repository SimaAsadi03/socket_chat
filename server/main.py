import socket
import threading
from common.config import HOST, PORT

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()
            print(f"[SERVER] From {addr}: {msg}")

            if msg.lower() == "/exit":
                print(f"[SERVER] Client {addr} requested to disconnect")
                break

            # Send to others
            broadcast(f"[Message from {addr}]: {msg}", conn)

    except:
        pass
    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"[SERVER] Connection closed from {addr}")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    run_server()
