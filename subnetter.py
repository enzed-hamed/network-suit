#!/usr/bin/env python3
# Python program to validate an Ip address

# re module provides support
# for regular expressions
import re


class GetSubnetMask:
    # Defining Regex patterns to capture all possible combinations of subnet/mask

    # For validating an Ip-address and
    regex_subnet = "^(\ )*((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\ )*$"
    # For validating an IP-address proceded with CIDR subnet mask notation
    regex_subnet_mask_cidr = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])((\ )*\/(\ )*((\d)|((1|2)\d)|(3(0|1|2))))$"
    # For validation of mask - cird notation
    regex_mask_cidr = "^((1|2)\d)|(3(1|2))$"
    # For validation of subnet mask (network address)
    regex_mask_doted_decimal = "^((128|192|224|240|248|252|254)\.0\.0\.0)|(255\.(((0|128|192|224|240|248|252|254)\.0\.0)|(255\.(((0|128|192|224|240|248|252|254)\.0)|255\.(0|128|192|224|240|248|252|254)))))$"
    # For validation of Network address and Subnet mask in doted decimal notation
    regex_subnet_mask_doted_decimal = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\ )*((128|192|224|240|248|252|254)\.0\.0\.0)|(255\.(((0|128|192|224|240|248|252|254)\.0\.0)|(255\.(((0|128|192|224|240|248|252|254)\.0)|255\.(0|128|192|224|240|248|252|254)))))$"

    # Define a function for
    # validate an Ip address

    def __init__(self):
        self.subnet = ""
        self.mask = ""
        self.__mask_type = ""

        self.__get_subnet_mask()
        self.__subnet_standard()

    def subnetting(self):
        # Getting number of host bits in base subnet
        hosts = self.__mask_standard()
        # Getting subnetting plan from user
        print("[+] Subnetting could be done as follow: (chose one plan)\n")
        for selection in range(hosts):
            print(
                "{} - You can subnet your network into  {}  networks with each having  {}  hosts.".format(
                    selection, 2**selection, 2 ** (hosts - selection)
                )
            )

        selection = int(input("\n[+] Select a plane: \n > "))

        # Make a local '.' seperated binary list version of subnet
        subnet = self.subnet.split(".")
        for portion in range(4):
            subnet[portion] = "{:08b}".format(int(subnet[portion]))

        # Main loop for calculating and printing special addresses of each subnet
        print("[+] Subnetting is done! Your addresses are as  follow:")
        for network in range(2**selection):
            print("*** {}st Network:".format(network + 1))

            # Two for loops for setting network bits and zeroing the host bits
            # Hense producing network address of new subnet
            for bit in range(32 - hosts, 32 - hosts + selection + 1):
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8]
                    + "{:08b}".format(network)[bit - (32 - hosts + (8 - selection))]
                    + subnet[bit // 8][bit % 8 + 1 :]
                )

            for bit in range(32 - hosts + selection, 32):
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "0" + subnet[bit // 8][bit % 8 + 1 :]
                )

            print(
                "Network address:     {}".format(
                    ".".join(str(int(portion, 2)) for portion in subnet)
                )
            )

            # For loop for setting host bits to 'one' in order to produce
            # Proadcast address
            for bit in range(32 - hosts + selection, 32):
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "1" + subnet[bit // 8][bit % 8 + 1 :]
                )

            print(
                "Proadcast address:   {}".format(
                    ".".join(str(int(portion, 2)) for portion in subnet)
                )
            )

            # Two for loop for producing first and last address

            # Produce first address
            for bit in range(32 - hosts + selection, 31):
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "0" + subnet[bit // 8][bit % 8 + 1 :]
                )
            else:
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "1" + subnet[bit // 8][bit % 8 + 1 :]
                )
            print("Assignable addresses are in the range:\n", end=" " * 40)
            print(
                "{}".format(".".join(str(int(portion, 2)) for portion in subnet)),
                end="",
            )

            # Produce last address
            for bit in range(32 - hosts + selection, 31):
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "1" + subnet[bit // 8][bit % 8 + 1 :]
                )
            else:
                subnet[bit // 8] = (
                    subnet[bit // 8][: bit % 8] + "0" + subnet[bit // 8][bit % 8 + 1 :]
                )
            print(
                " - {}".format(".".join([str(int(portion, 2)) for portion in subnet])),
                end="\n\n",
            )

    def __mask_standard(self):
        ones = 0
        if self.__mask_type == "decimal dotted":
            for portion in self.mask.split("."):
                ones += "{:b}".format(int(portion)).count("1")
            else:
                zeros = 32 - ones
        elif self.__mask_type == "cidr":
            ones = int(self.mask)
            zeros = 32 - ones

        return zeros

    def __subnet_standard(self):
        subnet = self.subnet
        self.subnet = ""

        if self.__mask_type == "decimal dotted":
            for portion in range(4):
                self.subnet += str(
                    int(subnet.split(".")[portion]) & int(self.mask.split(".")[portion])
                )
                self.subnet += "."
            else:
                self.subnet = self.subnet.strip(".")

        elif self.__mask_type == "cidr":
            for portion in range(0, int(self.mask) // 8):
                self.subnet += subnet.split(".")[portion] + "."

            self.subnet += str(
                (2**9 - 2 ** (8 - int(self.mask) % 8))
                & int(subnet.split(".")[int(self.mask) // 8])
            )

            for portion in range(int(self.mask) // 8 + 1, 4):
                self.subnet += "." + str(0)

        print("************************ {}".format(self.subnet))

    def get_subnet(self):
        return self.subnet

    def get_mask(self):
        return self.mask

    def __get_subnet_mask(self):
        flag = 1
        while flag:
            addr = input("[+] Please specify your network: \n > ")

            if re.search(self.regex_subnet_mask_cidr, addr):
                subnet, mask = addr.split("/")
                subnet = subnet.split()[0]
                mask = mask.split()[0]
                self.__mask_type = "cidr"
                print("--> Subnet: {} , Mask: {}".format(subnet, mask))
                flag = 0

            elif re.search(self.regex_subnet_mask_doted_decimal, addr):
                subnet, mask = addr.split()
                self.__mask_type = "decimal dotted"
                print("--> Subnet: {} , Mask: {}".format(subnet, mask))
                flag = 0

            elif re.search(self.regex_subnet, addr):
                subnet = addr.split()[0]
                print("--> Subnet: {}".format(subnet))
                flag = 2

            else:
                print("[-] Inputted Address is invalid.\n")
                flag = 1

            while flag == 2:
                addr = input("[+] Please specify mask for the network: \n > ")
                if re.search(self.regex_mask_doted_decimal, addr):
                    mask = addr.strip()
                    self.__mask_type = "decimal dotted"
                    print("--> Mask: {}".format(mask))
                    flag = 0
                elif re.search(self.regex_mask_cidr, addr):
                    # mask = addr.split("/")[1]
                    mask = addr
                    mask = mask.strip()
                    self.__mask_type = "cidr"
                    print("--> Mask: {}".format(mask))
                    flag = 0
                else:
                    print("[-] Inputed mask is invalid.\n")

        self.subnet = subnet
        self.mask = mask


if __name__ == "__main__":
    network = GetSubnetMask()

    print("---------> {}".format(network.get_subnet()))
    print("---------> {}".format(network.get_mask()))

    network.subnetting()
