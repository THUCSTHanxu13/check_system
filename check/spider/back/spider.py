#!/usr/bin/env python
# -*- coding: utf-8 -*-
import docx
from docx import *
import urllib2
import sys;
sys.path
import re


		
	relationships = relationshiplist()
	document = newdocument()
	body = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
	#统一为unicode编码
	cc = 0
	print len(paratextlist)
	for context in paratextlist:
		context = context.strip()
		if len(context) == 0:
			continue
		cc += 1
		print "processing paragraph ", cc, len(paratextlist)
		if cc == 1 and len(context) < 20:
			body.append(heading(context, 2))
			continue
		con_split=sentencen_split(context)
		con_backup=''
		con_similar=''
		res=''
		paralist = list()
		tu = ("            ", '')
		paralist.append(tu)
		for i in con_split:
			con_backup=con_backup+i
			if len(i) <= 10:
				tip = 0
			else:
				tip = check(i)
		#	para=paragraph(re.sub("#","\n",i))
		#	body.append(para)
		#	print tip
			if (tip>limit):			  
				res=res+i
		#		print "(" + re.sub("#","\n",i) + "(" + str(tip*100) + ")" + ", 'b')"
				tu = (i + "(%d%%)"%(tip*100), 'b')
				paralist.append(tu)
		#		para1 = paragraph("(%d%%)"%(tip*100))
		#		body.append(para1)
			else:
				tu = (i, '')
				paralist.append(tu)
			jindu=int(len(con_backup)/float(len(context))*100)
			print "%d%%" % (jindu)
		body.append(paragraph(paralist))
	








	print "0"
	




	title    = u'入党材料检测结果'
	subject  = u''
	creator  = u'admin'
	keywords = [u'检测']
	print "1"
	
	coreprops = coreproperties(title=title, subject=subject, creator=creator,
                               keywords=keywords)
							   
	print "2"
	
	savedocx(document, coreprops, appproperties(), contenttypes(), websettings(),
             wordrelationships(relationships), outfile)
	
	print "3"
	return "%d%%" % (len(res)/float(len(con_backup))*100)
def test():
	print "haha"

# print spider("-d 1.docx -o 1.gg.docx")
