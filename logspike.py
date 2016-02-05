#!/usr/bin/env python

import sys, os, socket, time, re, selects

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
                if index == token_pos:
                    rebuilt_string += crypto.encode(cipher_key, token)
                else:
                    rebuilt_string += token
            return rebuilt_string
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

    while True:
        #Accept incoming connection
        conn, addr = in_socket.accept()

        #Create blank buffer
        input_buffer = ""

        #Receive data
        while True:
            try:
                #Test connection
                ready_to_read, ready_to_write, in_error = \
                    select.select([conn,], [conn,], [], 5)
            except select.error:
                #Close connection on failure detection, and return to outer loop
                conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                conn.close()
                print("Client closed connection.\nListening...")
                break

            #Append to the buffer
            input_buffer += conn.recv(buffer_size)

            #Split the buffer into lines (keeping line breaks)
            lines = input_buffer.splitlines(True)

            #Iterate through the lines
            for line in lines:
                #If this line doesn't end with a new line, then we should assume
                #that it's incomplete, and we append it to the buffer again
                if not line.endswith("\n"):
                    input_buffer = line
                    print "Incomplete line, putting back in buffer"
                    continue
                #Otherwise, search for tokens to replace with encoded values
                output_message = replace(line)
                print("output message: " + output_message)
                #Send to output socket
                out_socket.sendto(output_message,out_socket_address)
            input_buffer = ""

if __name__ == "__main__":
    with open(keyfile,'r') as f:
        cipher_key = f.read()
    compile_patterns()
    main()
