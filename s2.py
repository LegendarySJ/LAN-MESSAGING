# Import required modules
import socket
import threading

HOST = '0.0.0.0'  # Listen on all available interfaces within the LAN
PORT = 9999  # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message:
            if message.startswith('@'):
                dest_username, message = message.split(maxsplit=1)
                dest_username = dest_username[1:]  # Remove '@' from username
                send_message_to_user(username, dest_username, message)
            else:
                final_msg = f"[{username}]: {message}"
                send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")
            break

# Function to send message to a single client
def send_message_to_user(sender_username, dest_username, message):
    for user in active_clients:
        if user[0] == dest_username:
            user[1].sendall(f"[{sender_username} to {dest_username}]: {message}".encode())
            break

# Function to send message to all clients
def send_messages_to_all(message):
    for user in active_clients:
        user[1].sendall(message.encode())

# Function to handle client
def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = f"SERVER: {username} joined the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
