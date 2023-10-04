def validate_ip(addr):
    section = addr.split('.')

    if len(section) != 4:
        print("IP Address {} is not valid".format(addr))
        return False

    for sec in section:
        try:
            isinstance(int(sec), int)
        except ValueError:
            print("IP Address {} is not valid".format(addr))
            return False

        if int(sec) < 0 or int(sec) > 255:
            print("IP Address {} is not valid".format(addr))
            return False

    print("IP Address {} is valid".format(addr))
    return True


input_ip = input("[+] Please enter the IP Address: ")
validate_ip(input_ip)
