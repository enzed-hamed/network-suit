from IPy import IP

ip = "127.0.0.2.5"

try:
    IP(ip)
    print('Valid')
except ValueError:
    print('Invalid')
