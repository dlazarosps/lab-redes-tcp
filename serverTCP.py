# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket
import time
import argparse
from datetime import datetime
from threading import Thread

def servidor(ip,porta):
	FLAG = True
	TCP_IP = ip
	TCP_PORT = porta

	BUFFER_SIZE = 10 * (2**10)

	#instancia socket 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(5)

	# data arquivo de log
	times = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H:%M')
	
	def client(conn, addr):
		log_file = 'tcp_{}_{}.log'.format(addr[1],times)
		# fp = open(log_file, 'w')
		n_pac = 0
		diff = 0
		init = time.time()
		while FLAG:
			data = conn.recv(BUFFER_SIZE)	
			n_pac += len(data)

			if not data: 
				break

			end = time.time()
			diff = (end-init)
			
			if diff >= 1:
			# band = (n_pac * 8) / diff
				band = ((n_pac * 8) // int(diff))
				# print('%0.2f \t' % band)
				if band >= 2 ** 30:
					# fp.write("%0.2f Gbps \n" % (10 * band / 10 ** 9))
					print("%0.2f Gbps \t port %d \n" % (band / 10 ** 9, addr[1]))
				elif band <  2 ** 30 and band >= 2 ** 20:
					# fp.write("%0.2f Mbps \n" % (10 * band / 10 ** 7))
					print("%0.2f Mbps \t port %d \n" % (band / 10 ** 6, addr[1]))
				elif band < 2 ** 20 and band >= 2 ** 10:
					# fp.write("%0.2f Kbps \n" % (10 * band / 1000))
					print("%0.2f Kbps \t port %d \n" % (band / 1000, addr[1]))
				else:
					# fp.write("%0.2f bps \n" % (band)) 				
					print("%0.2f bps \t port %d \n" % (band, addr[1]))
				n_pac = 0
				# diff = 0
				init = time.time()
				# time.sleep(1)
				
		# fp.close() 
		conn.close()
			
	try:
		while True:
			conn, addr = s.accept()
			print('Endereco de conexao: {}'.format(addr))
			Thread(target=client, args=(conn,addr)).start()
			time.sleep(10)
	except:
		FLAG = False
		s.close()
		exit(0)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Cliente - Equidade de trafego de rede.')
	parser.add_argument('-i', '--ip', type=str, help='número de IP do servidor', required=True)
	parser.add_argument('-p', '--port', type=int, help='Porta TCP', required=True)

	args = parser.parse_args()
	servidor(args.ip, args.port)