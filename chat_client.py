#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "[Team 9]"
__credits__ = [
  "Nima Mahanloo",
  "Dawn Petersen",
  "Armondo Lopez"
  "Christopher Loi"
]

# Import statements
import socket as s
import ssl
import sys

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = sys.argv[1]
server_port = 12000

def main():
  # Create socket
  context=ssl.create_default_context()
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  ssocket=context.wrap_socket(client_socket, server_hostname=server_name)

  try:
    # Establish TCP connection
    ssocket.connect((server_name,server_port))
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)

  # Get input from user
  user_input = input('Input lowercase sentence:')

  # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
  try:
    # Set data across socket to server
    #  Note: encode() converts the string to UTF-8 for transmission
    ssocket.send(user_input.encode())

    # Read response from server
    server_response = ssocket.recv(1024)
    # Decode server response from UTF-8 bytestream
    server_response_decoded = server_response.decode()

    # Print output from server
    print('From Server:')
    print(server_response_decoded)

  finally:
    # Close socket prior to exit
    client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()