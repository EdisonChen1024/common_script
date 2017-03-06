#!/usr/local/python
# coding=utf8

# std
import urllib2 as url_lib
import threading
import os
# 3rd
from bs4 import BeautifulSoup

dir_raw = "./raw_data"
dir_produce = "./produce_data"
max_page = 73219
fm = '''http://so.gushiwen.org/view_%d.aspx'''
l_error_page = []
l_ok_page = []

def get_one_page(num):
	response = url_lib.urlopen(fm % num)
	html = response.read()
	if "该文章不存在或已被删除" in html:
		print "error_page:", num
		l_error_page.append(num)
		return

	l_ok_page.append(num)
	soup = BeautifulSoup(html, "html.parser")
	ps = soup.prettify().encode("utf8")
	# print ps.encode("utf8")
	fd_raw = file("%s/%d.txt" % (dir_raw, num), "w")
	fd_raw.write(ps)
	fd_raw.close()

def batch(left, right):
	l_thread = []
	for num in xrange(left, right + 1):
		t = threading.Thread(target = get_one_page, args = (num, ) )
		l_thread.append(t)

	for t in l_thread:
		t.start()

	for t in l_thread:
		t.join()	

def download_all_page(start = 1, end = max_page):
	step = 20
	for num in xrange(start, end + 1, step):
		left  = num
		right = num + step - 1
		if right > max_page:
			right = max_page

		batch(left, right)

def log():
	l_error_page.sort()
	l_ok_page.sort()
	fd = file("log.txt", "w")
	fd.write("error_page:%05d|%s\n" % (len(l_error_page), l_error_page) )
	fd.write("   ok_page:%05d|%s\n" % (len(l_ok_page), l_ok_page) )
	fd.close()

l_html = []
def parse():
	print "read..."
	for root, dirs, files in os.walk(dir_raw):
		for file_name in files:
			full_name = os.path.join(root, file_name)
			fd = file(full_name, "r")
			html = fd.read()
			fd.close()
			l_html.append(html)

			soup = BeautifulSoup(html, "html.parser")
			time = ""
			author = ""
			title = soup.body.h1.string
			s = soup.find_all("div", class_ = "main3")
			s = s[0].div
			print s.encode("gbk")
			print s
			print "8==============>"
			print time, author, title 
			return

# download_all_page()
# log()
parse()
print("All done.")
# os.system("pause")
# os.system("shutdown /s /t 30")
