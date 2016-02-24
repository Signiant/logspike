#!/usr/bin/env python

import sys, os, socket, time, re, select, syslog, traceback

#Contains the encode and decode methods
import crypto

#Has the configurable parameters
from config import *

#Has the patterns and replace token positions
from patterns import match_patterns

#Compiled patterns with token position
compiled_patterns = list()

#Look for a pattern match, if matched find the token we want to replace and
#encode it. Reconstruct the message and return.
def replace(message):
    try:
        for pattern, token_pos in compiled_patterns:
            matched = pattern.match(message)
            if matched:
                rebuilt_string = ""
                for index, group in enumerate(matched.groups(), start=1):
                    if index in token_pos:
                        token = matched.group(index)
                        sub_token = crypto.encode(token.strip())
                        rebuilt_string += sub_token
                        continue
                    rebuilt_string += group
                return rebuilt_string
        #If none of the patterns match, return the original message
    except Exception as e:
        try:
            exc_info = sys.exc_info()
            syslog.syslog("Logspike: ERROR -------------- " + str(e))
            syslog.syslog(traceback.print_exception(*exc_info))
            exit(1)
        except:
            syslog.syslog("Logspike: Fatal Error! Could not get Traceback information.")
    return message

def compile_patterns():
    #This gets the pattern to match, and the token position (in regex groups)
    #to obfuscate
    syslog.syslog("Searching for the following patterns:")
    for pattern, token_pos in match_patterns:
        #Compile the pattern and add it to the list
        syslog.syslog(pattern + " @ position(s): " + str(token_pos))
        compiled_pattern = re.compile(pattern, flags=(re.M))
        if isinstance(token_pos, (int, long)):
            token_pos = [token_pos]
        pattern_tuple = (compiled_pattern, token_pos)
        compiled_patterns.append(pattern_tuple)

def main():
        #Input TCP socket
        in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Set socket re-use
        in_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Outgoing UDS socket
        out_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        syslog.syslog("Logspike: Starting lockspike.")
        syslog.syslog("Logspike: Input address:  " + in_socket_address + ":" + str(in_socket_port))
        syslog.syslog("Logspike: Output address: " + out_socket_address)

        #Bind the incoming TCP socket with the specified port from the config
        in_socket.bind((in_socket_address,in_socket_port))

        #Listen and allow no backlog of connections (refuse any more than the current)
        in_socket.listen(0)


    while True:
        #Sleep for two seconds just in case we get into a loop. Don't want to
        #tie up resources
        time.sleep(2)

        syslog.syslog("Logspike: Listening...")

        #Accept incoming connection
        conn, addr = in_socket.accept()

        #Don't allow socket to block
        conn.setblocking(0)

        #Create blank buffer
        input_buffer = ""

        #Receive data
        while True:

            #Set the timeout for receiving log messages
            ready = select.select([conn], [], [], connection_timeout)

            #If we're not ready to read, or in error
            if not ready[0] or ready[2]:
                syslog.syslog("Logspike: Lost connection to input socket")
                break

            #Flag to know if we need to clear the buffer or not
            clear_buffer = True

            #Flag to know if the
            close_connection = True

            #Append to the buffer
            input_buffer += conn.recv(buffer_size)

            if not input_buffer:
                continue

            #Split the buffer into lines (keeping line breaks)
            lines = input_buffer.splitlines(True)

            #Iterate through the lines
            for line in lines:
                #If this line doesn't end with a new line, then we should assume
                #that it's incomplete, and we add it to the beginning of the buffer
                if not line.endswith("\n"):
                    input_buffer = line
                    clear_buffer = False
                    continue
                #Otherwise, search for tokens to replace with encoded values
                output_message = replace(line).strip()
                #Send to output socket
                out_socket.sendto(output_message,out_socket_address)
            if clear_buffer:
                input_buffer = ""

if __name__ == "__main__":
    try:
        compile_patterns()
        main()
    except Exception as e:
        try:
            exc_info = sys.exc_info()
            syslog.syslog("Logspike: ERROR -------------- " + str(e))
            syslog.syslog(traceback.print_exception(*exc_info))
            exit(1)
        except:
            syslog.syslog("Logspike: Fatal Error! Could not get Traceback information.")
