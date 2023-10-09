#!/usr/bin/env python3

import requests
import socket, ssl
import threading


class Proxy:
	def __init__(self, port=8000):
		self.port = port
		self.buffer_size = 4096

		self.proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def run(self):
		self.proxy_sock.bind(("0.0.0.0", self.port))
		self.proxy_sock.listen(100)
		print("[+] Proxy server is running on port {}".format(self.port))

		while True:
			client, addr = self.proxy_sock.accept()
			print("-> {} : {}".format(addr[0], addr[1]))
			threading.Thread(target=self.process_request, args=(client,), daemon=True).start()
	
	def process_request (self, client):
		payload = client.recv(self.buffer_size)
		host = payload.decode().split("\r\n")[1].split(" ")[1]

		server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		server.connect((host, 80))
		server.sendall(payload)
		server_data = server.recv(4 * 4096)
		# print(server_data)
		server.close()

		client.sendall(server_data)
		client.close()


if __name__ == "__main__":
	proxy = Proxy(8000)
	proxy.run()

