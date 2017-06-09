# coding=utf8
import socket
import threading

host = "0.0.0.0"
port = 10241
max_client = 1024

def agent(obj):
	size = 1024 # 和客户端一致
	obj.settimeout(3)
	while True:
		try:
			buff = obj.recv(1024)
			obj.send(buff)
		except Exception as e:
			print "disconnect:", obj.fileno(), address, e
			break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(max_client)
print "Listen at %s:%s max client:%d" % (host, port, max_client)
while True:
	obj, address = server.accept()
	print "new client:", obj.fileno(), address
	t = threading.Thread(target = agent, args = [obj])
	t.start()
