import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("💬 Socket Chat Client")
        self.master.configure(bg="#f0f0f0")
        self.connected = False

        # نام‌کاربری
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.master)
        if not self.username:
            messagebox.showinfo("Exit", "Username is required")
            self.master.destroy()
            return

        # اتصال
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
            self.sock.sendall(f"/username {self.username}".encode())
            self.connected = True
        except Exception:
            messagebox.showerror("Connection Error", "Could not connect to the server.")
            self.master.destroy()
            return

        # ناحیه‌ی چت
        self.text_area = scrolledtext.ScrolledText(master,
            wrap=tk.WORD, width=60, height=20,
            bg="#BDDDE4", fg="black", font=("Helvetica", 11))
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

        # فیلد ورودی
        self.message_entry = tk.Entry(master, width=40, font=("Helvetica", 11))
        self.message_entry.pack(padx=10, pady=(0,5))
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        # دکمه‌ها
        btn_frame = tk.Frame(master, bg="#f0f0f0")
        btn_frame.pack(pady=5)
        self.send_btn = tk.Button(btn_frame, text="Send", command=self.send_message,
                                  bg="#4CAF50", fg="white", width=10)
        self.send_btn.pack(side=tk.LEFT, padx=5)
        self.users_btn = tk.Button(btn_frame, text="Users", command=self.request_users,
                                   bg="#009688", fg="white", width=10)
        self.users_btn.pack(side=tk.LEFT, padx=5)
        self.exit_btn = tk.Button(btn_frame, text="Exit", command=self.exit_chat,
                                  bg="#f44336", fg="white", width=10)
        self.exit_btn.pack(side=tk.RIGHT, padx=5)

        # شنیدن پیام‌ها
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def disable_on_disconnect(self):
        """غیرفعال کردن ورودی و دکمه‌ها و اعلام قطع اتصال"""
        if self.connected:
            self.connected = False
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, "[SERVER] Disconnected from server.\n")
            self.text_area.config(state=tk.DISABLED)
            self.message_entry.config(state=tk.DISABLED)
            self.send_btn.config(state=tk.DISABLED)
            self.users_btn.config(state=tk.DISABLED)

    def receive_messages(self):
        while True:
            try:
                raw = self.sock.recv(1024)
                if not raw:
                    raise ConnectionError
                message = raw.decode()
                timestamp = datetime.now().strftime("%H:%M")
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, f"[{timestamp}] {message}\n")
                self.text_area.yview(tk.END)
                self.text_area.config(state=tk.DISABLED)
            except Exception:
                self.disable_on_disconnect()
                break

    def send_message(self):
        if not self.connected:
            return
        msg = self.message_entry.get().strip()
        if not msg:
            return
        try:
            self.sock.sendall(msg.encode())
            # نمایش خودکار پیام
            timestamp = datetime.now().strftime("%H:%M")
            prefix = "You"
            if msg.startswith("/pm "):
                prefix = "Private"
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"[{timestamp}] {prefix}: {msg}\n")
            self.text_area.yview(tk.END)
            self.text_area.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)
        except Exception:
            self.disable_on_disconnect()

    def request_users(self):
        if not self.connected:
            return
        try:
            self.sock.sendall("/users".encode())
        except Exception:
            self.disable_on_disconnect()

    def exit_chat(self):
        try:
            if self.connected:
                self.sock.sendall("/exit".encode())
                self.sock.close()
        except:
            pass
        self.master.destroy()

def run_client_gui():
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    run_client_gui()
