import sys, os, socket, time, random

out_socket_address = "/tmp/logspike"

try:
    os.unlink(out_socket_address)
except OSError:
    if os.path.exists(out_socket_address):
        print("Deleting old input socket.")
        #Just delete it
        os.remove(out_socket_address)

read_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
read_socket.bind(out_socket_address)

while True:
    print read_socket.recv(1024)
