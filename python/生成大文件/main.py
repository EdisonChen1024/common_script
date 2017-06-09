# coding=utf8
import sys

# 文件大小(GB)
if len(sys.argv) > 1:
	size = int(sys.argv[1])
else:
	size = 0

# 文件数量
if len(sys.argv) > 2:
	amount = int(sys.argv[2])
else:
	amount = 1

def create(size, amount):
	# 一次写入1G
	word = "01"
	txt = word * (1024 * 1024 * 1024 * 1 / len(word))	
	def write(file_name):
		fd = file(file_name, "w")
		for x in xrange(1, size + 1):
			fd.write(txt)

		fd.close()
		print file_name, "Done"

	if amount > 1:
		for x in xrange(1, amount + 1):
			file_name = "%d-%dG.txt" % (x, size)
			write(file_name)
	else:
		file_name = "%dG.txt" % size
		write(file_name)


create(size, amount)
print "All Done."
