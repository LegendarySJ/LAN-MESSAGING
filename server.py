import socket
import threading

# Dictionary to store client sockets and their addresses
client_sockets = {}

def receive_messages(client_socket, client_name):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                # Check if message is intended for another client
                if data.startswith("@"):
                    recipient, message = data.split(" ", 1)
                    recipient = recipient[1:]
                    if recipient in client_sockets:
                        recipient_socket = client_sockets[recipient]
                        recipient_socket.send(f"{client_name}: {message}".encode())
                    else:
                        client_socket.send("Error: Recipient not found.".encode())
                # Check if message is intended for all clients
                elif data.startswith("#"):
                    message = data[1:]
                    for name, sock in client_sockets.items():
                        if name != client_name:  # Exclude sender
                            sock.send(f"{client_name}: {message}".encode())
                else:
                    print(f"{client_name}: {data}")
        except Exception as e:
            print(f"Error receiving message from {client_name}: {e}")
            break

def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    client_name = client_socket.recv(1024).decode()
    client_sockets[client_name] = client_socket

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_name))
    receive_thread.start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))  # Change the port if needed
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
