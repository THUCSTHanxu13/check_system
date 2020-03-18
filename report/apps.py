from django.apps import AppConfig
from django.conf import settings


class ReportConfig(AppConfig):
    name = 'report'
    verbose_name = '疫情防控'

    def ready(self):
        if settings.DEBUG or hasattr(settings, 'WECHATWORK_ROBOT_POST_URL'):
            from .signals import notify_on_person
