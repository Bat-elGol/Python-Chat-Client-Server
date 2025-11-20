
import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((host, port))
        except ConnectionRefusedError:
            print("Unable to connect to server.")
            exit()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    print("Disconnected from server.")
                    break
                print(message)
            except Exception as e:
                print(f"Error: {e}")
                break

    def send_messages(self):
        try:
            while True:
                message = input()
                if message.lower() == 'exit':
                    self.client_socket.send(message.encode())
                    print("Exiting...")
                    break
                self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            self.client_socket.close()

    def start(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()

if __name__ == "__main__":
    client = ChatClient()
    client.start()
