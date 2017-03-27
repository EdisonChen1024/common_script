# coding=utf8

# std
import socket
import threading

def run(iNum = 0):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 10241))
	size = 1024 # 和服务端一致
	fm = "%0" + str(size) + "s"
	s.send(fm % iNum)
	count = 0
	while True:
		data = s.recv(size)
		s.send(data)
		count += 1
		print "==================>", count


amount = 8
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
