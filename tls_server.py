
#! /usr/bin/python3 

# Imports
import http.server 
import ssl
import sys

# Variables, including location of server certificate and private key file 
server_address = sys.argv[1]
server_port = 443
ssl_key_file = sys.argv[1][4:] + "-key.pem"
ssl_certificate_file = sys.argv[1][4:] + "-cert.pem"

#Context is the TLS Server with its certificate file and key file location 
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 
context.load_cert_chain(ssl_certificate_file, ssl_key_file)

## Don't modify anything below
httpd = http.server.HTTPServer((server_address, server_port), http.server.SimpleHTTPRequestHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print("Listening on port", server_port) 
httpd.serve_forever()
  