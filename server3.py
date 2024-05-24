import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Server's IP address
PORT = 9999  # Port to listen on
LISTENER_LIMIT = 10  # Maximum number of simultaneous connections
PASSWORD = "passwd"  # Password for authentication (consider changing for security)
active_clients = []  # List to store active client connections
groups = {}  # Dictionary to store group information (name: password)

# Function for XOR encryption/decryption
def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(char) ^ key) for char in data)

# Function to send messages to a specific group
def send_messages_to_group(message, key, group_code):
    for user in active_clients:
        if user[2] == group_code:
            user[1].sendall(xor_encrypt_decrypt(message, key).encode())

# Function to listen for messages from a client
def listen_for_messages(client, username, key, group_code):
    while True:
        message = xor_encrypt_decrypt(client.recv(2048).decode('utf-8'), key)
        if message:
            if message.startswith("exit:"):
                # Handle exit request
                _, exit_group_code = message.split(":")
                if exit_group_code == group_code:
                    for i, user in enumerate(active_clients):
                        if user[0] == username and user[2] == group_code:
                            del active_clients[i]
                            break
                    client.sendall("Exit successful".encode())
                    prompt_message = f"SERVER: {username} has left the group {group_code}"
                    send_messages_to_group(prompt_message, key, group_code)
                else:
                    client.sendall("Invalid exit request".encode())
            elif message.startswith('@'):
                dest_username, message = message.split(maxsplit=1)
                dest_username = dest_username[1:]
                send_message_to_user(username, dest_username, message, key)
            else:
                final_msg = f"[{username}]: {message.split(':', maxsplit=1)[0]}"
                send_messages_to_group(final_msg, key, group_code)
        else:
            print(f"The message sent from client {username} is empty")
            break

# Function to send a message to a specific user
def send_message_to_user(sender_username, dest_username, message, key):
    for user in active_clients:
        if user[0] == dest_username:
            user[1].sendall(xor_encrypt_decrypt(f"[{sender_username} to {dest_username}]: {message.split(':', maxsplit=1)[0]}", key).encode())
            break

# Function to handle a client connection
def client_handler(client, key):
    while True:
        data = xor_encrypt_decrypt(client.recv(2048).decode('utf-8'), key)
        if data:
            username, group_code, password, action = data.split(':')
            if action == "create":
                if group_code in groups:
                    client.sendall("Group name already exists".encode())
                    client.close()
                    break
                else:
                    groups[group_code] = password
                    active_clients.append((username, client, group_code))
                    prompt_message = f"SERVER: {username} created and joined the group {group_code}"
                    send_messages_to_group(prompt_message, key, group_code)
                    break
            elif action == "join":
                if group_code in groups and groups[group_code] == password:
                    active_clients.append((username, client, group_code))
                    prompt_message = f"SERVER: {username} joined the chat"
                    send_messages_to_group(prompt_message, key, group_code)
                    break
                else:
                    client.sendall("Invalid group name or password".encode())
                    client.close()
                    break
            else:
                print(f"Invalid action from client {username}")
                client.sendall("Invalid action".encode())
                client.close()
                break
        else:
            print("Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client, username, key, group_code)).start()

# Main function to run the server
def main():
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
        threading.Thread(target=client_handler, args=(client, 5)).start()  # Consider using a more secure key management

if __name__ == '__main__':
    main()
