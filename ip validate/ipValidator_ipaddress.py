import ipaddress

def validate_ip(addr):
    try:
        ip = ipaddress.ip_address(addr)
        print("IP Address {} is valid. The object returned is {}".format(addr, ip))
    except ValueError:
        print("IP Address {} is not valid".format(addr))



ip = input("[+] Please enter an IP Address: ")
validate_ip(ip)
