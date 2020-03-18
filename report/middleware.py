from django.conf import settings
from django.utils import timezone

from . import utils
from .models import Record


class IPRecordMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/admin/'):
            return response
        person = getattr(request.user, 'person', None)
        if not person:
            return response
        Record.objects.get_or_create(
            person=person,
            date=utils.local_date(timezone.now() + settings.RECORD_OFFSET),
            defaults={'ip': utils.get_client_ip(request)},
        )
        return response
