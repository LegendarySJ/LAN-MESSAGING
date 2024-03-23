import socket
import threading

# Simple XOR encryption and decryption functions
def xor_encrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def xor_decrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                decrypted_data = xor_decrypt(data, 10)  # XOR decryption with key 10
                print('\n')
                print(decrypted_data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message(client_socket):
    while True:
        message = input("Enter your message : ")
        if message.startswith("@"):  # Check if the message is intended for another client
            client_socket.send(message.encode())
        elif message.startswith("#"):  # Check if the message is intended for all clients
            client_socket.send(message.encode())
        else:
            encrypted_message = xor_encrypt(message, 10)  # XOR encryption with key 10
            client_socket.send(encrypted_message.encode())

def start_client():
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port: "))
    client_name = input("Enter your name: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.send(client_name.encode())

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Start a thread to send messages
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()
