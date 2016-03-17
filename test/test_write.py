import sys, os, socket, time, random, string

in_socket_address = "127.0.0.1"
in_socket_port = 22222

write_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

write_socket.connect((in_socket_address, in_socket_port))

with open("sample.log", "r") as f:
    for string in f.readlines():
        print("Sending message: " + string)
        write_socket.send(string)
write_socket.close()
