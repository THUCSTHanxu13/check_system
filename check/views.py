from django.shortcuts import render, HttpResponse
from django.core.files import File
from .models import Person

from check.tasks import analyze_docx_file
import time
import random
import os
import json

SAVED_FILES_DIR = './check/spider/upload/'
RESULT_FILES_DIR = './check/spider/download/'
history = {}

def index(request):
    # person = request.user.person
    return render(request, 'check/index.html')

def wait(request):
    # person = request.user.person
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            uid = request.POST.get('uid', 0)
            if uid in history:
                download_name = history[uid]['download_name']
                if os.path.isfile(download_name):
                    result = {"status": 1}
                    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
                else:
                    result = {"status": 0}
                    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
            else:
                result = {"status": -1}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            result = {"status": -1}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

def upload(request):
    # person = request.user.person
    file = request.FILES.get("filename", None)
    if not file:
        return render(request, 'check/index.html')

    last_name = file.name.strip().split(".")[-1]
    name = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
    name = name + "_%d"%((int)(random.random()*10000)) 
    upload_name = os.path.join(SAVED_FILES_DIR, name + "." + last_name)
    download_name = os.path.join(RESULT_FILES_DIR, name + "." + last_name)
    json_name = os.path.join(RESULT_FILES_DIR, name + ".json" ) 

    res = {}
    res['uid'] = name
    res['real_name'] = file.name.strip()
    res['upload_name'] = upload_name
    res['download_name'] = download_name
    res['json_name'] = json_name
    history[res['uid']] = res

    with open(upload_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    analyze_docx_file.delay(res)
    return render(request, "check/wait.html", {'info': res})

def download(request, uid):
    # person = request.user.person
    if uid in history:
        res = history[uid]
        res['download_name'] = res['download_name'].strip('.')
        f = open(res['json_name'], "r")
        html_info = json.loads(f.read())
        f.close()
        return render(request, "check/download.html", {'info': res, 'html_info':html_info})
    else:
        return render(request, 'check/index.html')

def getfile(request, filename):
    # person = request.user.person
    file_pathname = os.path.join(RESULT_FILES_DIR, filename)
    with open(file_pathname, 'rb') as f:
        file = File(f)
        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)
    return response