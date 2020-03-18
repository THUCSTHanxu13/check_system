import datetime
import pathlib

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

import requests
from requests_oauthlib import OAuth2Session
from django_tables2 import RequestConfig
from django_tables2.export import TableExport

from . import utils
from .models import Person, Record, Entry, Building
from .forms import ProfileForm, RecordForm, EntryForm
from .tables import RecordTable, EntryTable, BuildingTable, BuildingEntryTable


def oauth_login(request):
    redirect_uri = request.build_absolute_uri(reverse('report:oauth_callback'))
    redirect_uri = redirect_uri.replace('http://', 'https://')  # XXX: Enforce HTTPS
    oauth = OAuth2Session(
        settings.OAUTH_CLIENT_ID,
        redirect_uri=redirect_uri,
    )
    authorization_url, state = oauth.authorization_url(settings.OAUTH_AUTHORIZE_URL)
    request.session['oauth_state'] = state
    return redirect(authorization_url)


def oauth_callback(request):
    redirect_uri = request.build_absolute_uri(reverse('report:oauth_callback'))
    redirect_uri = redirect_uri.replace('http://', 'https://')  # XXX: Enforce HTTPS
    oauth = OAuth2Session(
        settings.OAUTH_CLIENT_ID,
        redirect_uri=redirect_uri,
        state=request.session['oauth_state'],
    )
    authorization_response = request.build_absolute_uri()
    authorization_response = authorization_response.replace('http://', 'https://')  # XXX: Enforce HTTPS
    token = oauth.fetch_token(
        settings.OAUTH_ACCESS_TOKEN_URL,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        authorization_response=authorization_response,
    )
    request.session['oauth_token'] = token
    response = oauth.request('GET', settings.OAUTH_USER_INFO_URL)
    data = response.json()
    idnum = data['user']['student_id']
    try:
        user = utils.get_or_create_user(idnum)
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    except Person.DoesNotExist:
        messages.warning(request, '工作证号 {} 不在数据库中，请与本单位信息员联系。'.format(idnum))
    return redirect('report:home')


def tsinghua_auth_login(request):
    ipaddr = utils.get_client_ip(request).replace('.', '_')
    request.session['ipaddr'] = ipaddr
    url = settings.TSINGHUA_AUTH_LOGIN_URL.format(
        appid_md5=settings.TSINGHUA_AUTH_APPID_MD5,
        seq=settings.TSINGHUA_AUTH_SEQ,
        callback_url=reverse('report:tsinghua_auth_callback'),
    )
    return redirect(url)


def tsinghua_auth_callback(request):
    ticket = request.GET['ticket']
    url = settings.TSINGHUA_AUTH_AUTHORIZE_URL.format(
        appid=settings.TSINGHUA_AUTH_APPID,
        ticket=ticket,
        ipaddr=request.session['ipaddr'],
    )
    resp = requests.get(url)
    with (pathlib.Path(settings.BASE_DIR) / 'var' / 'tsinghua_auth.log').open('a') as log_file:
        log_file.write('{} {}\n'.format(datetime.datetime.now(), resp.text))
    data = {k: v for k, v in [p.split('=') for p in resp.text.split(':')]}
    code = data.get('code')
    if code == '0':
        idnum = data['zjh']
        try:
            user = utils.get_or_create_user(idnum)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except Person.DoesNotExist:
            messages.warning(request, '工作证号 {} 不在数据库中，请与本单位信息员联系。'.format(idnum))
    else:
        messages.error(request, '清华统一用户登录系统返回代码错误（{}），请与系统管理员联系。'.format(code))
        print('Tsinghua auth error: {}'.format(resp.text))
    return redirect('report:home')


def login(request):
    return render(request, 'report/login.html')


@login_required
def home(request):
    return render(request, 'report/home.html')


@login_required
def profile(request):
    person = request.user.person
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, '信息提交成功。')
            return redirect('report:home')
    else:
        form = ProfileForm(instance=person)
    return render(request, 'report/profile.html', {'form': form})


@login_required
def record_list(request):
    person = getattr(request.user, 'person')
    table = RecordTable(person.record_set.filter(is_submitted=True))
    RequestConfig(request).configure(table)
    return render(request, 'report/record_list.html', {'table': table})


@login_required
def record_detail(request):
    person = getattr(request.user, 'person')
    record, _ = Record.objects.get_or_create(
        person=person,
        date=utils.local_date(timezone.now() + settings.RECORD_OFFSET),
        defaults={'ip': utils.get_client_ip(request)},
    )
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.is_submitted = True
            record.save()
            messages.success(request, '健康打卡成功。')
            return redirect('report:record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'report/record_detail.html', {'form': form, 'submitted': record.is_submitted})


@login_required
def entry_list(request):
    person = getattr(request.user, 'person')
    table = EntryTable(person.entry_set.all())
    RequestConfig(request).configure(table)
    return render(request, 'report/entry_list.html', {'table': table})


@login_required
def entry_detail(request, entry_id=None):
    person = getattr(request.user, 'person')
    entry = None if entry_id is None else person.entry_set.get(pk=entry_id)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.person = person
            entry.approve1_decision = None
            entry.approve1_person = None
            entry.approve1_time = None
            entry.approve2_decision = None
            entry.approve2_person = None
            entry.approve2_time = None
            entry.approve3_decision = None
            entry.approve3_person = None
            entry.approve3_time = None
            entry.save()
            messages.success(request, '申请提交成功。')
            return redirect('report:entry_list')
    else:
        initial = {'date': utils.local_date(timezone.now() + settings.ENTRY_OFFSET)}
        last = person.entry_set.order_by('add_time').last()
        if last:
            initial['building'] = last.building
            initial['room'] = last.room
            initial['purpose'] = last.purpose
        form = EntryForm(instance=entry, initial=initial)
    return render(request, 'report/entry_detail.html', {'form': form})


@login_required
def entry_delete(request, entry_id):
    person = getattr(request.user, 'person')
    entry = person.entry_set.get(pk=entry_id)
    entry.delete()
    return redirect('report:entry_list')


@login_required
def building_list(request):
    table = BuildingTable(Building.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'report/building_list.html', {'table': table})


def building_detail(request, building_uuid, date=None):
    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    else:
        date = timezone.localdate()
    building = Building.objects.get(uuid=building_uuid)
    entries = building.entry_set.filter(date=date, approve3_decision=True)
    table = BuildingEntryTable(entries)
    RequestConfig(request, paginate=False).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('{}.{}'.format(date, export_format))
    context = {
        'building': building,
        'date': date,
        'prev_day': date - datetime.timedelta(days=1),
        'next_day': date + datetime.timedelta(days=1),
        'table': table,
    }
    return render(request, 'report/building_detail.html', context)
