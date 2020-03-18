from django.shortcuts import render, HttpResponse
from check.tasks import analyze_docx_file
import time
import random
import os

SAVED_FILES_DIR = './check/spider/upload/'

def ask(request):
    print ("=====================")
    analyze_docx_file.delay("./check/spider/upload/test.docx")
    print ("----------------------")
    return HttpResponse("hx")
    # return render(request, 'notice/index.html', {
    #     'notices': Notice.objects.filter(published=True).order_by('-post_time'),
    # })

def index(request):
    return render(request, 'check/index.html')

def upload(request):
    file = request.FILES.get("filename", None)
    if not file:
        return render(request, 'check/index.html')

    last_name = file.name.strip().split(".")[-1]
    print (last_name)
    name = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
    name = name + "_%d"%((int)(random.random()*10000)) 

    pathname = os.path.join(SAVED_FILES_DIR, name + "." + last_name)
    
    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    res = {}
    res['real_name'] = file.name.strip()
    res['upload_name'] = pathname
    res['uid'] = name

    return HttpResponse("hx")
