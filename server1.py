import socket
import threading

# Simple XOR encryption and decryption functions
def xor_encrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def xor_decrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

# Dictionary to store client sockets and their addresses
client_sockets = {}

def send_to_client(sender_name, recipient_name, message):
    recipient_socket = client_sockets.get(recipient_name)
    if recipient_socket:
        encrypted_message = xor_encrypt(f"{sender_name}: {message}", 10)  # XOR encryption with key 10
        recipient_socket.send(encrypted_message.encode())
    else:
        return f"Error: Recipient '{recipient_name}' not found."

def send_to_all(sender_name, message):
    encrypted_message = xor_encrypt(f"{sender_name}: {message}", 10)  # XOR encryption with key 10
    for name, sock in client_sockets.items():
        if name != sender_name:
            sock.send(encrypted_message.encode())

def receive_messages(client_socket, client_name):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                # Check if message is intended for another client
                if data.startswith("@"):
                    recipient, message = data.split(" ", 1)
                    recipient = recipient[1:]
                    response = send_to_client(client_name, recipient, message)
                    if response:
                        client_socket.send(response.encode())
                # Check if message is intended for all clients
                elif data.startswith("#"):
                    message = data[1:]
                    send_to_all(client_name, message)
                else:
                    decrypted_data = xor_decrypt(data, 10)  # XOR decryption with key 10
                    print(f"{client_name}: {decrypted_data}")
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
