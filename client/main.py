import socket
import threading
from common.config import HOST, PORT

def receive_messages(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            print(data.decode())
    except Exception:
        pass  # برای جلوگیری از خطای ناگهانی در هنگام بستن اتصال

def send_messages(client):
    try:
        while True:
            msg = input()
            client.sendall(msg.encode())

            if msg.strip().lower() == "/exit":
                print("[CLIENT] Disconnected from chat.")
                break

    except Exception as e:
        print(f"[CLIENT ERROR]: {e}")

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("[CLIENT] Connected to the server.")

        # Start receiving thread
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        # Handle sending messages
        send_messages(client)

if __name__ == "__main__":
    run_client()
