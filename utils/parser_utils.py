#coding:utf-8

from pyltp import Segmentor
from pyltp import SentenceSplitter
from .utils import *

class parser_utils(object):

	def __init__(self, path):
		self.segmentor = Segmentor()  # 初始化实例
		self.segmentor.load(path + '/cws.model') # 加载模型

	def convert_to_unicode(self, text, plain = False):
		text = convert_to_unicode(text)
		text = clean_text(text, plain)
		text = tokenize_chinese_chars(text)
		return text

	def segment(self, text):
		words = list(self.segmentor.segment(text))
		return words

	def sentencesplit(self, text):
		sentences = SentenceSplitter.split(text)
		return sentences

	def textcheck(self, txt_t, txt_w):
		txt_t = self.convert_to_unicode(txt_t, plain = True)
		txt_w = self.convert_to_unicode(txt_w, plain = True)
		txt_t = self.segment(txt_t)
		txt_w = self.segment(txt_w)
		acc = 0.0
		total = 0.0
		for word in txt_t:
			if word in txt_w:
				acc += 1.0
			total += 1.0
		return acc / total