import iptools


ip = '127.0.0.1'

c_ip = iptools.ipv4.validate_ip(ip)

if c_ip is True:
    print("Valid")
else:
    print("Invalid")
