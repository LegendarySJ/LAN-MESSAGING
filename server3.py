import socket
import threading

HOST = '0.0.0.0'
PORT = 9999
LISTENER_LIMIT = 5
active_clients = []

def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(char) ^ key) for char in data)

def listen_for_messages(client, username, key):
    while True:
        message = xor_encrypt_decrypt(client.recv(2048).decode('utf-8'), key)
        if message:
            if message.startswith('@'):
                dest_username, message = message.split(maxsplit=1)
                dest_username = dest_username[1:]
                send_message_to_user(username, dest_username, message, key)
            else:
                final_msg = f"[{username}]: {message}"
                send_messages_to_all(final_msg, key)
        else:
            print(f"The message sent from client {username} is empty")
            break

def send_message_to_user(sender_username, dest_username, message, key):
    for user in active_clients:
        if user[0] == dest_username:
            user[1].sendall(xor_encrypt_decrypt(f"[{sender_username} to {dest_username}]: {message}", key).encode())
            break

def send_messages_to_all(message, key):
    for user in active_clients:
        user[1].sendall(xor_encrypt_decrypt(message, key).encode())

def client_handler(client, key):
    while True:
        username = xor_encrypt_decrypt(client.recv(2048).decode('utf-8'), key)
        if username:
            active_clients.append((username, client))
            prompt_message = f"SERVER: {username} joined the chat"
            send_messages_to_all(prompt_message, key)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, key)).start()

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
        threading.Thread(target=client_handler, args=(client, 5)).start()

if __name__ == '__main__':
    main()
