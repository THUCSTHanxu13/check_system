# Reporting System for 2019-nCoV Control in Spring 2020

### 安装pyltp

1. 从github上下载pyltp

2. 从github上下载ltp，把ltp解压之后，替代pyltp中的ltp文件夹

3. 进入pyltp，执行python setup.py install

### 安装celery和redis

1. pip 安装 celery

2. sudo apt-get update

3. sudo apt-get install redis-server

### 运行redis

1. 开启后台托管程序，如screen

2. redis-server

### pyltp的模型下载

1. http://ltp.ai/download.html

2. 下载ltp_data_v3.4.0.zip	

3. 将压缩包里面的模型都放置到 ./check/spider/models/ 下

### Django 与 celery

0. 启动redis后

1. 进入到spring2020文件夹下

2. python manage.py migrate django_celery_results

3. celery -A spring2020 worker -l info

运行后屏幕里出现下面内容即为成功

	[tasks]
	  . check.tasks.analyze_docx_file
	  . spring2020.celery.debug_task

### Django

后续内容与正常django没有区别