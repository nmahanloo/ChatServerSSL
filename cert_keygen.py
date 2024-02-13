#!/usr/bin/python

"""CA Issuer for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Nima Mahanloo",
    "Dawn Petersen",
    "Armondo Lopez",
    "Christopher Loi"
]

import subprocess as sp
import os
from mininet.log import setLogLevel, info


def create_cert(cn, server_ip):


    # Store CN without 'www.' in a variable
    cn_name = cn
    if cn[:4] == "www.":
        cn_name = cn[4:]

    #info('*** Generate a new 2048-bit RSA private key for your server.\n')
    cmd = 'sudo openssl genrsa -out ' + cn_name + '-key.pem 2048'
    os.system(cmd.encode())

    info('*** Generate a certificate signing request to “send” to the root CA.\n')
    cmd = 'sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -key ' \
          + cn_name + '-key.pem -out ' \
          + cn_name + '.csr ' \
          + '-subj "/C=US/ST=CA/L=Seaside/O=CST311/OU=PA4/CN=' + cn + '"'
    os.system(cmd.encode())

    info('*** Use the Root CA to create the X.509 server certificate that is valid for 365 days and sign it.\n')
    cmd = 'sudo openssl x509 -req -days 365 -in ' + cn_name \
          + '.csr -CA ' + '/etc/ssl/demoCA' + '/' + 'cacert.pem -CAkey ' \
          + '/etc/ssl/demoCA/private/cakey.pem -CAcreateserial -out ' \
          + cn_name + '-cert.pem'
    os.system(cmd.encode())

    
    info('*** Add CN to the Mininet VM’s host file.\n')
    host = server_ip + '        ' + cn
    newline=[]
    # opening and creating new .txt file
    with open('/etc/hosts', 'r') as re:
        lines = re.readlines()
        for line in lines:
            #isspace() function
            if line.strip() == '':
                newline.append(host)
                newline.append('\n\n')
            else:
                newline.append(line)
    with open('/etc/hosts', 'w') as wr:
        for line in newline:
            wr.writelines(line)


def main():

    print("Note: This program issues CA certificates \nfor the PA4's web server and chat server automatically.\n"
          + "Please be prepare to enter a pass phrase multiple times for \nthe certificates during the process.\n")

    info('*** Get CN for the web server from user.\n')
    cn_webserver = input("Enter the CN for the web server> ")

    info('*** Get CN for the chat server from user.\n')
    cn_chatserver = input("Enter the CN for the chat server> ")

    info('*** Create certificate for the webserver.\n')
    create_cert(cn_webserver, '10.0.3.3')

    info('*** Create certificate for the chatserver.\n')
    create_cert(cn_chatserver, '10.0.5.3')

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()