#coding:utf-8
from __future__ import absolute_import, unicode_literals

from .spider import docx_analyzer
import json
import time

analyzer = docx_analyzer(model_path = './check/spider/models/', driver_path = "./check/spider/drivers/", upload_path = './check/spider/upload/', download_path = './check/spider/download/')

# 导入celery_app
from spring2020 import celery_app

# @shared_task
@celery_app.task
def analyze_docx_file(docx_info):
    print ("Starting to analyze the input docx file")
    docx_file = docx_info['upload_name']
    all_res, rate = analyzer.analyze_docx(docx_file)
    
    # for i in range(2):
    #     time.sleep(1)
    #     print ("------------")
    # f = open("./check/spider/test.json", "r")
    # a = json.loads(f.read())
    # all_res, rate = a
    # f.close()

    html_info = analyzer.export_to_html(all_res, rate)
    download_name = analyzer.export_to_docx(all_res, rate, docx_info['download_name'])

    f = open(docx_info['json_name'], "w")
    f.write(json.dumps(html_info))
    f.close()

    print ("Finishing analyzing the input docx file " + download_name)
    return docx_info
