import os

#TCP socket info
in_socket_address = "127.0.0.1"
in_socket_port = 22222

#UDS location
out_socket_address = "/tmp/logspike"

#Increase or decrease for the predicted max message size
buffer_size = 2048

#Connection timeout in seconds (3 days)
connection_timeout = 259200
