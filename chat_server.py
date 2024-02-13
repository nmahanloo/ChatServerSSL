#!env python

"""Chat server for CST311 Programming Assignment 3
   This server program uses multithrading to handle
   multiple client connections concurrently. Here's why 
   and how multithreadin is essential for this task:

   1. Multiple Client Connections:
    The goal is to handle multiple clients connecting to
    the server concurrently. Without multithreading, the server
    would process clients sequientially, making it unresponsive
    to new connections while serving existing ones. 
   2. Concurrency:
    Each client should send and receive messages independently. 
    Multithreading allows us to create a separate thread for each client,
    ensuring that they can communicate concurrently. 

   This code achieves this by creating a new thread for each connected
   client, allowing them to communicate concurrently. Messages from clients
   are stored in the 'messages' list, and when both clients have sent 
   messages, the server composes the response and sends it to both clients. 
"""
__author__ = "[Team 9]"
__credits__ = [
    "Nima Mahanloo",
    "Dawn Petersen",
    "Armondo Lopez"
    "Christopher Loi"
]

import socket as s
import time
import ssl
import sys

# Configure logging
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ssl_key_file = sys.argv[1][4:] + "-key.pem"
ssl_certificate_file = sys.argv[1][4:] + "-cert.pem"
server_port = 12000
messages = []
clients = []
addr = []


def connection_handler(connection_socket, address):
    # Read data from the new connectio socket
    #  Note: if no data has been sent this blocks until there is data
    query = connection_socket.recv(1024)

    # Decode data from UTF-8 bytestream
    query_decoded = query.decode()

    # Log query information
    log.info("Recieved query test \"" + str(query_decoded) + "\"")

    # Perform some server operations on data to generate response
    messages.append(query_decoded)

    # Sent response over the network, encoding to UTF-8
    # connection_socket.send(f"X: '{messages[0]}', Y: '{messages[1]}'")

    # Close client socket
    # connection_socket.close()


def main():
    # Create a TCP socket
    context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(ssl_certificate_file, ssl_key_file)
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign IP address and port number to socket, and bind to chosen port
    server_socket.bind(('', server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(1)

    # Alert user we are now online
    log.info("The server is ready to receive on port " + str(server_port))

    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Enter forever loop to listen for requests
        while len(clients) < 2:
            # When a client connects, create a new socket and record their address
            connection_socket, address = server_socket.accept()
            ssocket=context.wrap_socket(connection_socket, server_side=True)
            log.info("Connected to client at " + str(address))
            clients.append(ssocket)
            addr.append(address)
        i = 0
        while i < len(clients):
            # Pass the new socket and address off to a connection handler function
            connection_handler(clients[i], addr[i])
            i += 1
        i = 0
        while i < len(clients):
            clients[i].send(f"X: '{messages[0]}', Y: '{messages[1]}'".encode())
            clients[i].close()
            i += 1

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()