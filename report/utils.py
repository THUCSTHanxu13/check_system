import csv

from django.conf import settings
from django.contrib import auth
from django.utils import timezone

import requests
import ipware

from .models import Person


geoip2 = None
if hasattr(settings, 'GEOIP_PATH'):
    from django.contrib.gis.geoip2 import GeoIP2
    geoip2 = GeoIP2()


def city_of_ip(ip):
    try:
        info = geoip2.city(ip)
        return info['city']
    except:
        return None


def export_as_csv(queryset, out):
    fields = (
        'idnum', 'name', 'grade', 'teaching_class',
        'gender', 'dob', 'category', 'ethnicity', 'nationality', 'political', 'province', 'high_school', 'future',
        'phone', 'father_phone', 'mother_phone', 'location', 'dorm', 'temp_dorm',
        'remark',
    )
    writer = csv.DictWriter(out, fields, extrasaction='ignore')
    writer.writeheader()
    for person in queryset:
        writer.writerow(person.__dict__)


def send_notification(content):
    if settings.DEBUG:
        print(content)
    if hasattr(settings, 'WECHATWORK_ROBOT_POST_URL'):
        requests.post(settings.WECHATWORK_ROBOT_POST_URL, json={
            'msgtype': 'text',
            'text': {
                'content': content,
            },
        })


def get_client_ip(request):
    ip, _ = ipware.get_client_ip(request)
    return ip


def get_or_create_user(idnum):
    person = Person.objects.get(idnum=idnum)
    user = person.user
    if not user:
        User = auth.get_user_model()
        user = User.objects.create_user(idnum, first_name=person.name)
        person.user = user
        person.save(update_fields=('user',))
    return user


def local_date(timestamp=None):
    if timestamp is None:
        timestamp = timezone.now()
    return timezone.make_naive(timestamp).date()
