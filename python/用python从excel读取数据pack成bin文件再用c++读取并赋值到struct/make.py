# coding=utf8

# 3rd
import xlrd
# std
import math
import os
import struct


# excel配置表路径
path_excel = r"."
# 输出的路径
path_out = r"."
# cpp读取配置需要的头文件名
head_name = "config.h"
# excel配置表转换成二进制文件之后的后缀名 A.xlsx ==> A.suffix
suffix = ".bin"


#####################################################################################
# make
#####################################################################################
# 类型定义
int32_t = "int32_t"
int64_t = "int64_t"
char = "char"


def get_file_name(file_name):
	if file_name.endswith("xlsx") and ("~" not in file_name):
		# 去掉后缀
		l = file_name.split(".")
		return l[0]
	else:
		return ""


def num2char(num):
	'''
	@note 1-26 映射 A-Z, 主要用于显示excel中的列名
	'''
	s = None
	if num <= 26:
		s = chr(ord("A") + num - 1)
	else:
		s = num

	return s


# Cell objects have three attributes: ctype is an int, value (which depends on ctype) and xf_index. If "formatting_info" is not enabled when the workbook is opened, xf_index will be None. The following table describes the types of cells and how their values are represented in Python.
# Type symbol	Type number	Python value
# XL_CELL_EMPTY   	0	empty string u''
# XL_CELL_TEXT	    1	a Unicode string
# XL_CELL_NUMBER	2	float
# XL_CELL_DATE	    3	float
# XL_CELL_BOOLEAN	4	int; 1 means TRUE, 0 means FALSE
# XL_CELL_ERROR	    5	int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
# XL_CELL_BLANK	    6	empty string u''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.
def cell_type_to_name(cell_type):
	if cell_type == xlrd.book.XL_CELL_EMPTY:
		return "XL_CELL_EMPTY"
	elif cell_type == xlrd.book.XL_CELL_TEXT:
		return "XL_CELL_TEXT"
	elif cell_type == xlrd.book.XL_CELL_NUMBER:
		return "XL_CELL_NUMBER"
	elif cell_type == xlrd.book.XL_CELL_DATE:
		return "XL_CELL_DATE"
	elif cell_type == xlrd.book.XL_CELL_BOOLEAN:
		return "XL_CELL_BOOLEAN"
	elif cell_type == xlrd.book.XL_CELL_ERROR:
		return "XL_CELL_ERROR"
	elif cell_type == xlrd.book.XL_CELL_BLANK:
		return "XL_CELL_BLANK"
	else:
		return "type_unknown"


# 检查一列都是同一个类型
def check_col(file_name, sheet, expect_type, col, row_start = 1):
	# 判空
	if expect_type == xlrd.book.XL_CELL_EMPTY:
		print "error: [%s][%s,%s] cell is null..." % ( file_name, row_start + 1, num2char(col + 1) ) 
		os.system("pause")
		return False
	# 日期格式需要纯文本
	if expect_type == xlrd.book.XL_CELL_DATE:
		print "error: [%s][%s,%s] cell type is date, please use pure text..." % ( file_name, row_start + 1, num2char(col + 1) ) 
		os.system("pause")
		return False
	# 检查一列
	for r in xrange(row_start, sheet.nrows):
		cell = sheet.cell(r, col)
		if expect_type != cell.ctype:
			print "error: [%s][%s,%s] type not the same, expect_type:%s, cell_type:%s" % (file_name, r + 1, num2char(col + 1), cell_type_to_name(expect_type), cell_type_to_name(cell.ctype))
			os.system("pause")
			return False

	return True


# d= {
# 	excel文件名: [ book, [(字段名, 类型(int or string), size), (), () ...] ],
#	...
# }
d = {} 


# 读取每个excel表
def read():
	max_int32 = math.pow(2, 31) - 1
	for root, dirs, files in os.walk(path_excel):
		for f in files:
			name = get_file_name(f)
			if name:
				full_name = os.path.join(root, f)
				book = xlrd.open_workbook(full_name)
				sheet = book.sheet_by_index(0)
				len_col = sheet.ncols
				len_row = sheet.nrows
				# 分析
				for i in xrange(len_col):
					cell_key = sheet.cell(0, i)
					cell_value = sheet.cell(1, i)
					type_name = None
					size = 512					
					if not check_col(f, sheet, cell_value.ctype, i):
						return
					# 如果是int, 看看是int32还是int64
					if cell_value.ctype == xlrd.book.XL_CELL_NUMBER:
						type_name = int32_t
						for j in xrange(1, len_row):
							cell = sheet.cell(j, i)
							if cell.value >= max_int32:
								type_name = int64_t
								break
					elif cell_value.ctype == xlrd.book.XL_CELL_TEXT:
						type_name = char
						for j in xrange(1, len_row):
							cell = sheet.cell(j, i)
							# 测试字符串长度时需要+1, cpp字符串末尾需要'\0'
							while (len(cell.value) * 3 + 1) > size:
								size = size * 2
					else:
						print("error: [%s][2, %s] unknow cell type:%d" % (f, num2char(i + 1), cell_value.ctype))
						os.system("pause")
						return

					d[name] = d.get(name, [None, []])
					d[name][0] = book
					d[name][1].append( (cell_key.value, type_name, size) )


# 生成cpp头文件
def write_head():
	keys = d.keys()
	keys.sort()
	fd_head = file(path_out + "/" + head_name, "w")
	fd_head.write("#pragma once\n");
	fd_head.write("#include <stddef.h>\n")
	fd_head.write("#include <time.h>\n")
	fd_head.write("#include <sys/types.h>\n")
	fd_head.write("#if !defined(_WIN32) && !defined(_WIN64)\n")
	fd_head.write("    #include <stdint.h>\n")
	fd_head.write("    #include <inttypes.h>\n")
	fd_head.write("#else\n")
	fd_head.write("    typedef  signed char             int8_t;\n")
	fd_head.write("    typedef  short                   int16_t;\n")
	fd_head.write("    typedef  int                     int32_t;\n")
	fd_head.write("    typedef unsigned char            uint8_t;\n")
	fd_head.write("    typedef unsigned short           uint16_t;\n")
	fd_head.write("    typedef unsigned int             uint32_t;\n")
	fd_head.write("    #if _MSC_VER >= 1300\n")
	fd_head.write("        typedef long long            int64_t;\n")
	fd_head.write("        typedef unsigned long long   uint64_t;\n")
	fd_head.write("    #else\n")
	fd_head.write("        typedef __int64              int64_t;\n")
	fd_head.write("        typedef unsigned __int64     uint64_t;\n")
	fd_head.write("    #endif\n")
	fd_head.write("#endif\n")
	fd_head.write("\n")
	fd_head.write("#pragma pack(1)\n");
	fd_head.write("\n")
	for k in keys:
		v = d[k]
		name = k
		book = v[0]
		fmt_list = v[1]
		fd_head.write("struct tag%s\n" % name)
		fd_head.write("{\n")
		for t in fmt_list:
			member_name = t[0]
			type_name = t[1]
			size = t[2]
			if type_name in (int32_t, int64_t):
				fd_head.write("    %s i%s;\n" % (type_name, member_name))
			else:
				fd_head.write("    char sz%s[%d];\n" % (member_name, size))

		fd_head.write("};\n")
		fd_head.write("\n\n\n")

	fd_head.write("#pragma pack()\n")
	fd_head.close()


# 生成二进制
def write_bin():
	keys = d.keys()
	keys.sort()
	for k in keys:
		v = d[k]
		name = k
		book = v[0]
		fmt_list = v[1]
		sheet = book.sheet_by_index(0)
		len_col = sheet.ncols
		len_row = sheet.nrows
		fd = file(path_out + "/" + name + suffix, "wb")
		# 构造格式
		fmt = "="
		for t in fmt_list:
			member_name = t[0]
			type_name = t[1]
			size = t[2]
			if type_name == int32_t:
				fmt += "i"
			elif type_name == int64_t:
				fmt += "q"
			else:
				fmt += str(size) + "s"
		# 写入结构体大小
		s = struct.pack("=i", struct.calcsize(fmt))
		fd.write(s)
		# 写入行数
		s = struct.pack("=i", len_row - 1)
		fd.write(s)
		# print name, "szie:%d" % struct.calcsize(fmt), "count:%d" % (len_row - 1)
		# 读取数据(跳过第一行)
		for r in xrange(1, len_row):
			l = []
			for c in xrange(len_col):
				cell = sheet.cell(r, c)
				if cell.ctype == xlrd.book.XL_CELL_TEXT:
					l.append(cell.value.encode("utf8"))
				else:
					l.append(cell.value)

			s = struct.pack(fmt, *l)
			fd.write(s)

		fd.close()


read()
print "read excel success..."
write_head()
print "write_head success..."
write_bin()
print "write_bin success..."

print "All Done..."
os.system("pause")
