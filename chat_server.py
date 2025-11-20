
import socket
import threading
from datetime import datetime

# Path to the text file for storing chat history
CHAT_LOG_FILE = "chat_log.txt"

# Initialize the chat log file
def init_chat_log():
    try:
        with open(CHAT_LOG_FILE, "x") as f:
            pass  # Create the file if it doesn't exist
    except FileExistsError:
        pass

# Log chat activity
def log_chat_activity(username, action, message=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_LOG_FILE, "a") as f:
        if action == "connect":
            f.write(f"[{timestamp}] {username} connected.\n")
        elif action == "disconnect":
            f.write(f"[{timestamp}] {username} disconnected.\n")
        elif action == "message":
            f.write(f"[{timestamp}] {username}: {message}\n")

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = {}

    def handle_client(self, client_socket, address):
        try:
            client_socket.send("Enter your username: ".encode())
            username = client_socket.recv(1024).decode().strip()

            if not username or username in self.clients:
                client_socket.send("Username invalid or already in use.\n".encode())
                client_socket.close()
                return

            self.clients[username] = client_socket
            log_chat_activity(username, "connect")
            print(f"{username} connected from {address}")
            client_socket.send(f"Welcome, {username}! Type 'exit' to leave.\n".encode())
            self.broadcast(f"{username} has joined the chat.", username)

            while True:
                try:
                    message = client_socket.recv(1024).decode()
                    if not message or message.lower() == 'exit':
                        break
                    log_chat_activity(username, "message", message)
                    self.broadcast(f"{username}: {message}", username)
                except ConnectionResetError:
                    break

        finally:
            if username in self.clients:
                del self.clients[username]
                log_chat_activity(username, "disconnect")
                self.broadcast(f"{username} has left the chat.", username)
            client_socket.close()
            print(f"{username} disconnected.")

    def broadcast(self, message, sender_username):
        for username, client_socket in self.clients.items():
            if username != sender_username:
                try:
                    client_socket.send(message.encode())
                except:
                    client_socket.close()
                    del self.clients[username]

    def start(self):
        print("Waiting for connections...")
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
            except KeyboardInterrupt:
                print("Shutting down server...")
                self.server_socket.close()
                break

if __name__ == "__main__":
    init_chat_log()
    server = ChatServer()
    server.start()
