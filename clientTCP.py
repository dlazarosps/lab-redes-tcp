# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket  
import argparse

def cliente(ip,porta):
	TCP_IP =  ip
	TCP_PORT = porta
	BUFFER_SIZE = 2 * 1024 # 10 * (2**10)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))

	while True:
		MESSAGE = (b'A'*BUFFER_SIZE)  # bytes(BUFFER_SIZE)
		s.send(MESSAGE)
		# data = s.recv(BUFFER_SIZE)
		# if not data: 
		# 	break
	s.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Cliente - Equidade de trafego de rede.')
	parser.add_argument('-i', '--ip', type=str, help='número de IP do servidor', required=True)
	parser.add_argument('-p', '--port', type=int, help='Porta TCP', required=True)

	args = parser.parse_args()
	cliente(args.ip, args.port)