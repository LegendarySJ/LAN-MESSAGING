import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            print('\n')
            print(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message(client_socket):
    while True:
        message = input("Enter your message : ")
        client_socket.send(message.encode())

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
