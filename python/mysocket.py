# coding=utf8

# std
import socket
import threading

def run(iNum = 0):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.110.3", 8888))
	while True:
		s.recv(1024)


amount = 1024 * 100
lThread = []
print("new...")
for i in xrange(amount):
	t = threading.Thread(target = run, args = [i])
	lThread.append(t)

print("start...")
for t in lThread:
	t.start()

print("join...")
for t in lThread:
	t.join()

print("All done.")
