import socket
import threading
from common.config import HOST, PORT

clients = []
usernames = {}  # سوکت → نام‌کاربری

def send_private(sender_sock, target_name, content):
    sender_name = usernames.get(sender_sock, "Unknown")
    for client in clients:
        if usernames.get(client) == target_name:
            try:
                client.sendall(f"[PM from {sender_name}]: {content}".encode())
                return True
            except:
                pass
    return False

def list_users(requester_sock):
    lines = []
    for client in clients:
        name = usernames.get(client, "Unknown")
        ip, port = client.getpeername()
        lines.append(f"{name} ({ip}:{port})")
    return "[SERVER] Connected users:\n" + "\n".join(lines)

def broadcast(message, sender_sock):
    for client in clients:
        if client is not sender_sock:
            try:
                client.sendall(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    clients.append(conn)
    usernames[conn] = f"{addr[0]}:{addr[1]}"

    try:
        while True:
            raw = conn.recv(1024)
            if not raw:
                break
            msg = raw.decode().strip()

            # تنظیم نام‌کاربری
            if msg.startswith("/username "):
                new_name = msg.split(" ", 1)[1].strip()
                usernames[conn] = new_name or usernames[conn]
                conn.sendall(f"[SERVER] Your username is set to '{usernames[conn]}'\n".encode())
                continue

            # درخواست لیست کاربران
            if msg.lower() == "/users":
                info = list_users(conn).encode()
                conn.sendall(info)
                continue

            # خروج
            if msg.lower() == "/exit":
                break

            # پیام خصوصی
            if msg.startswith("/pm "):
                parts = msg.split(" ", 2)
                if len(parts) == 3:
                    target, content = parts[1], parts[2]
                    if not send_private(conn, target, content):
                        conn.sendall(f"[SERVER] User '{target}' not found\n".encode())
                else:
                    conn.sendall(b"[SERVER] Usage: /pm <username> <message>\n")
                continue

            # پیام عمومی
            sender_name = usernames.get(conn, "Unknown")
            full = f"[{sender_name}]: {msg}".encode()
            broadcast(full, conn)
            print(f"[SERVER] Broadcast from {sender_name}: {msg}")

    except Exception as e:
        print(f"[SERVER] Error with {addr}: {e}")

    finally:
        print(f"[SERVER] {usernames.get(conn)} disconnected")
        clients.remove(conn)
        usernames.pop(conn, None)
        conn.close()

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
