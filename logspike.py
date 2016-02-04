#!/usr/bin/env python

import sys, os, socket, time, re

#Has the configurable parameters
from config import *

compiled_patterns = list()

def match(message):
    for pattern in compiled_patterns:
        matched = pattern.match(message)
        if matched:
            pass


def encrypt_token(input_token):
    pass

def compile_patterns:
    for pattern in match_patterns:
        #Compile the pattern and add it to the list
        compiled_patterns.append(re.compile(pattern))


def main():
    #Input TCP socket
    in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Outgoing UDS socket
    out_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    print ("Starting lockspike.")
    print ("Input address:  " + in_socket_address + ":" + str(in_socket_port))
    print ("Output address: " + out_socket_address)

    #Bind the incoming TCP socket with the specified port from the config
    in_socket.bind((in_socket_address,in_socket_port))

    #Listen and allow no backlog of connections (refuse any more than the current)
    in_socket.listen(0)

    print ("Listening...")

    conn, addr = in_socket.accept()

    while True:
        message = conn.recv(buffer_size)
        print("Processing message: " + message)
        time.sleep(0.05)
        processed_message = message + " -- processed"
        out_socket.sendto(processed_message,out_socket_address)
        #out_file.flush()

if __name__ == "__main__":
    compile_patterns()
    main()
