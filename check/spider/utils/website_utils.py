#coding:utf-8
import time
import re
import string
import requests
import urllib
from urllib.parse import quote

# from selenium import webdriver
# from fake_useragent import UserAgent

import bs4
from bs4 import BeautifulSoup
import ssl
import random

class website_utils(object):

	def __init__(self, path):
		ssl._create_default_https_context = ssl._create_unverified_context
		# 模拟浏览器
		# self.path = path + "/geckodriver"

	def get_html_from_url(self, url, timeout = 10, times = 5):
		while times != 0:
			# try:
				url = quote(url, safe = string.printable)
				req = urllib.request.Request(url)
				res = urllib.request.urlopen(req, timeout = timeout)
				html = res.read().decode('utf-8')
				return html
			# except Exception as err:
			# 	print ("time out!")
			# 	times -= 1
		return ""
		# 模拟浏览器
		# driver = webdriver.Firefox(executable_path = self.path)
		# driver.get(url)
		# time.sleep(0.5+random.random())
		# html = driver.page_source
		# time.sleep(0.5+random.random())
		# driver.quit()
		# return html

	# 百度查询接口，目前百度机器人检查过严，已废除
	# def get_baidu_ab_from_text(self, text):
	# 	text = re.sub("\s", "", text)
	# 	res = self.get_html_from_url(u'https://www.baidu.com/s?wd=' + text)
	# 	abstract = re.findall('''<div class="c-abstract"[^<^>]*?>[\S\s]*?<em>[\S\s]*?</em>[\S\s]*?</div>''', res)
	# 	res = []
	# 	for i in abstract:
	# 		con = re.sub("<.*?>","",i)
	# 		if con.find("zhidao")!=-1:
	# 			continue
	# 		if con.find(u"更多关于")!=-1:
	# 			continue
	# 		if con.find(u"答案")!=-1:
	# 			continue
	# 		res.append(con)
	# 	return res
	
	def get_sogou_ab_from_text_with_pages(self, text, pages):
		text = re.sub("\s", "", text)
		res = []
		for page in range(pages):
			html = self.get_html_from_url(u'https://www.sogou.com/outersearch?pid=sogou-wsse-7b16a52cf3727c22&page=' + str(page) + u'&ie=utf8&query=' + text)
			html = BeautifulSoup(html)
			ab_html = html.find_all('div', {'class':'rb'})
			for i in ab_html:
				try:
					url = 'https://www.sogou.com/' + i.find('a', {'name':'dttl'})['href']
					con = i.find('div', {'class':'ft'})
					con = con.get_text()
					con = re.sub("<.*?>","",con)
					con = re.sub("&.*?;","",con)
					res.append((con, url))
				except Exception as err:
					pass
				ab_html = html.find_all('div', {'class':'vrwrap'})
				for i in ab_html:
					try:
						url = 'https://www.sogou.com/' + i.find('h3').find('a')['href']
						con = i.find('p', {'class':'str_time'})
						con = con.get_text()
						con = re.sub("<.*?>","",con)
						con = re.sub("&.*?;","",con)
						res.append((con, url))
					except Exception as err:
						pass
		return res

	def get_sogou_ab_from_text_with_scope(self, text, limit, mode = "sogou"):
		pages = limit // 10 if limit % 10 == 0 else limit // 10 + 1
		if mode == "sogou":
			res = self.get_sogou_ab_from_text_with_pages(text, pages)
		# else:
			# res = self.get_sogou_ab_from_text_with_pages(text, pages)
		return res