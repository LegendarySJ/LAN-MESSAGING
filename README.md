# LAN-MESSAGING
In the realm of network communication, client-server architecture is a fundamental model for interaction between computers. It facilitates various applications like messaging systems, file sharing, and distributed computing. In this introduction, we'll elucidate a basic chat application employing Python's socket programming and threading for concurrent communication.

Client-Server Communication:
In a client-server architecture, multiple clients connect to a central server, which coordinates communication between them. The server acts as a mediator, receiving and dispatching messages among clients. Each client establishes a socket connection with the server through a designated port on the server machine.


Code Structure:

Server Code (server.py):

•	The server initializes a socket and binds it to a specific IP address and port.

•	It listens for incoming connections from clients.

•	Upon client connection, a new thread is spawned to handle communication with that client.

•	The server also keeps track of connected clients and forwards messages to the intended recipient.

Client Code (client.py):

•	The client prompts the user to enter the server's IP address, port, and their name.

•	Upon connection to the server, it initiates two threads:

  •	One thread listens for incoming messages from the server.

  •	Another thread allows the user to input messages to send to the server.

•	The client encrypts and sends messages to the server, and decrypts received messages for display.
Conclusion:

This chat application exemplifies the client-server model's versatility, offering real-time communication with encryption for enhanced security. By fostering understanding of socket programming and encryption techniques, this project provides a foundational platform for developing more advanced networked applications.

To enable client-to-client messaging in a client-server architecture, the server act as a mediator, relaying messages between clients. 

Client-to-Server Communication: Clients send messages to the server with the intended recipient's name prefixed to the message. For example, @recipient_name message_content.

If the messaage is sent with "#message_content the message" is forwarded to all the clients connected to the server.

Server Logic: The server receives messages from clients, parses them to determine the recipient, and forwards the message to the appropriate client.
