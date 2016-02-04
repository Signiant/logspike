import os

#TCP socket info
in_socket_address = "127.0.0.1"
in_socket_port = 22222

#UDS location
out_socket_address = "/tmp/logspike"

#Increase or decrease for the predicted max message size
buffer_size = 1024

#Ensure there are NO space characters in the key
keyfile_name = "cipher_key"

#Gets the keyfile from the same directory as this file
keyfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),keyfile_name)
