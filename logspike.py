#!/usr/bin/env python

import sys, os, socket, time, re

#Contains the encode and decode methods
import crypto

#Has the configurable parameters
from config import *

#Has the patterns and replace token positions
from patterns import match_patterns

#Compiled patterns with token position
compiled_patterns = list()

#Key is loaded from a file which is defined in the config
cipher_key = None

#Look for a pattern match, if matched find the token we want to replace and
#encode it. Reconstruct the message and return.
def replace(message):
    for pattern, token_pos in compiled_patterns:
        matched = pattern.match(message)
        if matched:
            rebuilt_string = ""
            for index, token in enumerate(matched.groups()):
                rebuilt_string += token
                if index == token_pos:
                    rebuilt_string += crypto.encode(cipher_key, token)
        else:
            return message

def compile_patterns():
    #This gets the pattern to match, and the token position (in regex groups)
    #to obfuscate
    for pattern, token_pos in match_patterns:
        #Compile the pattern and add it to the list
        print (pattern)
        compiled_pattern = re.compile(pattern)
        pattern_tuple = (compiled_pattern, token_pos)
        compiled_patterns.append(pattern_tuple)

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
        output_message = replace(message)
        out_socket.sendto(output_message,out_socket_address)

if __name__ == "__main__":
    with open(keyfile,'r') as f:
        cipher_key = f.read()
    compile_patterns()
    main()
