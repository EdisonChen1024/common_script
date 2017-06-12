# coding=utf8

# std
import time
import threading

# python -m pip install -U pip
# pip install websocket-client
# https://pypi.python.org/pypi/websocket-client/0.40.0
import websocket

# https://developers.google.com/protocol-buffers/
import proto.test_pb2 as pb


def fill_info(info):
	t = time.localtime()
	info.year = t.tm_year
	info.month = t.tm_mon
	info.day = t.tm_mday
	info.hour = t.tm_hour
	info.min = t.tm_min
	info.sec = t.tm_sec
	info.fmt = time.strftime("%Y-%m-%d %H:%M:%S", t)

def send(ws, proto):
	# max size is 64K
	# print(proto.ByteSize())
	ws.send(proto.SerializeToString(), websocket.ABNF.OPCODE_BINARY)

def on_open(ws):
	print "on_open"
	heartbeat = pb.msg_heartbeat()
	# int field
	heartbeat.count = 1
	# string field
	word = "01"
	heartbeat.padding = word * (1024 * 60 / len(word))
	# repeated field
	l = heartbeat.array
	for x in xrange(1024 * 1):
		l.append(x % 2)
	# nested field
	fill_info(heartbeat.info)
	send(ws, heartbeat)

def on_message(ws, message):
	print "on_message"
	# 反序列化
	heartbeat = pb.msg_heartbeat()
	heartbeat.ParseFromString(message)
	print heartbeat.count
	# 计数器
	heartbeat.count += 1
	fill_info(heartbeat.info)
	# 回包
	sec = 1
	time.sleep(sec)
	send(ws, heartbeat)

def on_close(ws):
	print "on_close", ws

def on_error(ws, error):
	print "on_error", error

# websocket.enableTrace(True)
def run():
	ws = websocket.WebSocketApp("ws://192.168.0.158:8888/hello_world",
		on_open = on_open,
		on_message = on_message,
		on_error = on_error,
		on_close = on_close)

	ws.run_forever(skip_utf8_validation = True)

# 多线程
l = []
amount = 1
for i in xrange(amount):
	t = threading.Thread(target = run)
	l.append(t)

for t in l:
	t.start()

for t in l:
	t.join()


print "All Done."
