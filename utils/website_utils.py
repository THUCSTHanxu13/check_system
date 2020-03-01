#coding:utf-8
import re
import string
import requests
import urllib
from urllib.parse import quote
from selenium import webdriver
import time
from fake_useragent import UserAgent
import bs4
from bs4 import BeautifulSoup
import ssl
import random

class website_utils(object):

	def __init__(self, path):
		ssl._create_default_https_context = ssl._create_unverified_context
		self.ua = UserAgent(verify_ssl=False)
		self.path = path + "/geckodriver"

	def get_html_from_url(self, url, timeout = 10, times = 5):
		# while times != 0:
		# 	try:
		# 		url = quote(url, safe = string.printable)
		# 		headers={"User-Agent": self.ua.random}
		# 		req = urllib.request.Request(url, headers=headers)
		# 		res = urllib.request.urlopen(req, timeout = timeout)
		# 		html = res.read().decode('utf-8')
		# 		time.sleep(0.1)
		# 		return html
		# 	except Exception as err:
		# 		print ("time out!")
		# 		times -= 1
		# return ""
		driver = webdriver.Firefox(executable_path = self.path)
		driver.get(url)
		time.sleep(0.5+random.random())
		html = driver.page_source
		time.sleep(0.5+random.random())
		driver.quit()
		return html

	def get_baidu_ab_from_text(self, text):
		text = re.sub("\s", "", text)
		res = self.get_html_from_url(u'https://www.baidu.com/s?wd=' + text)
		abstract = re.findall('''<div class="c-abstract"[^<^>]*?>[\S\s]*?<em>[\S\s]*?</em>[\S\s]*?</div>''', res)
		res = []
		for i in abstract:
			con = re.sub("<.*?>","",i)
			if con.find("zhidao")!=-1:
				continue
			if con.find(u"更多关于")!=-1:
				continue
			if con.find(u"答案")!=-1:
				continue
			res.append(con)
		return res

	def get_sogou_ab_from_text(self, text):
		text = re.sub("\s", "", text)
		html = self.get_html_from_url(u'https://www.sogou.com/web?query=' + text)
		html = BeautifulSoup(html)
		res = []

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
				# print ("err from get_sogou_ab_from_text")

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
				# print ("err from get_sogou_ab_from_text")

		next_page = html.find("a", {'id':'sogou_next'})
		if next_page:
			next_url = u'https://www.sogou.com/web' + next_page['href']
		else:
			next_url = None

		return res, next_url

	def get_sogou_ab_from_url(self, url):
		html = self.get_html_from_url(url)
		html = BeautifulSoup(html)

		res = []

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
				# print ("err from get_sogou_ab_from_url")

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
				# print ("err from get_sogou_ab_from_url")

		next_page = html.find("a", {'id':'sogou_next'})
		if next_page:
			next_url = u'https://www.sogou.com/web' + next_page['href']
		else:
			next_url = None

		return res, next_url

	def get_sogou_ab_from_text_with_scope(self, text, limit):
		# res = self.get_baidu_ab_from_text(text)
		res, next_url = self.get_sogou_ab_from_text(text)
		return res
		# while len(res) < limit and next_url != None:
		# 	res_new, next_url = self.get_sogou_ab_from_url(next_url)
		# 	res = res + res_new
		# print (res)
		# return res