import socket
from common.config import HOST, PORT

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("[CLIENT] Connected to the server.")
        
        while True:
            msg = input("Enter message to server (or 'exit' to quit): ")
            if msg.lower() == "exit":
                break
            client.sendall(msg.encode())
            data = client.recv(1024)
            print(f"[SERVER REPLY]: {data.decode()}")
        
        print("[CLIENT] Connection closed.")

if __name__ == "__main__":
    run_client()
