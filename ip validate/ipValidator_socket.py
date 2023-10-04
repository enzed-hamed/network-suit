import socket

ip = "127.0.0.1"

try:
    socket.inet_aton(ip)
    print('Valid')
except socket.error:
    print('Invalid')
