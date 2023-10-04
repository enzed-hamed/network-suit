#!/usr/bin/python3

import requests
import dns.resolver
#import scapy.all
from scapy.all import *
from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import random
import time


class traceroute:

    def __init__(self, domain=''):
        self.target_ip = ''
        self.target_domain = domain
        self.ip_country_dict = dict()
        self.ip_list = list()

        self.dns_lookup()
        self.tracer()
        self.ip_to_geolocation()
        self.show()
        
        

    def dns_lookup(self):
        self.gprint("\n> Resolving Domain Name Address ...")
        resolver_obj = dns.resolver.Resolver()
        resolver_obj.namespace = ["1.1.1.1"]
        lookup_result = resolver_obj.resolve(self.target_domain, 'A')
        self.target_ip = [ns.to_text() for ns in lookup_result][0]
        self.gprint("[+] DNS Resolution successfully finished.")
        self.gprint("--> {}\n".format(self.target_ip), slow=True)


    def tracer(self):
        self.gprint("\n> Tracing Routing Nodes to Target Host ...", normal=True)
        ttl = 1
        while(True):
            ip_packet = IP(ttl=ttl, dst=self.target_ip)
            ttl+=1
            recv_packet = sr1(ip_packet/TCP(), timeout=0.5, verbose=0)
            try:
#                self.ip_country_dict.upidate ({recv_packet.src: dict()})
                self.ip_list.append(recv_packet.src)
                if recv_packet.src == self.target_ip:
                    break
            except AttributeError:
#                self.ip_country_dict.update ({ttl : None})
                self.ip_list.append(ttl)
        self.gprint("[+] Node Tracing is Done.", normal=True)
        self.gprint("--> {} Nodes Identified.\n".format(len(self.ip_list)-1), normal=True)


    def ip_to_geolocation(self):
        print("\n> Looking up Database for Nodes IP Location ...")
#        for ip in filter(lambda item:isinstance(item, str), self.ip_country_dict.keys()):
#        for ip in filter(lambda x:x != '-', self.ip_list):
        for ip in filter(lambda item : isinstance(item, str), self.ip_list):
            ip_geolocation_obj = DbIpCity.get(ip, api_key='free')
            self.ip_country_dict.update({ip : dict()})
            self.ip_country_dict[ip].update({"country": ip_geolocation_obj.country})
            self.ip_country_dict[ip].update({"city": ip_geolocation_obj.city})
            self.ip_country_dict[ip].update({"region": ip_geolocation_obj.region})
        print("[+] Performing Lookup Successfully done.", end='\n\n')


    def show(self):
        for ip in self.ip_list:
            if isinstance(ip, str):
                print("\n## Node {:02}".format(self.ip_list.index(ip)+1))
                print("** IP - {}".format(ip))
                ccode = self.ip_country_dict[ip]["country"]
                try:
                    print("* Country - {} ({})".format(ccode, pycountry.countries.get(alpha_2=ccode).name))
                except AttributeError:
                    print("* Country - {} (Unknown - Address isn't yet assigned to any country)".format(ccode))
                print("* City - {}".format(self.ip_country_dict[ip]["city"]))
                print("* Region - {}".format(self.ip_country_dict[ip]["region"]))
            else:
                print("\n## Node {:02}".format(ip+1))
                print("[-] This Node Does NOT Respond.")
        else:
            print("\n## Target Host")
            print("** IP - {}  ({})".format(ip, self.target_domain))
            ccode = self.ip_country_dict[ip]["country"]
            try:
                print("* Country - {} ({})".format(ccode, pycountry.countries.get(alpha_2=ccode).name))
            except AttributeError:
                print("* Country - {} (Unknown - Address isn't yet assigned to any country)".format(ccode))
            print("* City - {}".format(self.ip_country_dict[ip]["city"]))
            print("* Region - {}".format(self.ip_country_dict[ip]["region"]))

        

    def gprint(self, string, fast=True, normal=False, slow=False):
        if slow:
            sec = 10
        elif normal:
            sec = 5
        else:
            sec = 0

        for char in string:
            print(char, end='', flush=True)
            time.sleep(random.randrange(sec, sec+5)/100)

        print()






tracer_opj = traceroute("google.com")
