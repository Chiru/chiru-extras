# UDP server example
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("", 5000))

print"UDPServer Waiting for client on port 5000"

while 1:
	data, address = server_socket.recvfrom(256)
	print "( " ,address[0], " " , address[1] , " ) said : ", data
