from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Person
from . import utils


@receiver(post_save, sender=Person)
def notify_on_person(sender, instance, created, update_fields, **kwargs):
    if created:
        return
    if update_fields is not None and tuple(update_fields) == ('user',):
        content = '{affiliation} {name} 注册了系统。当前共有 {num_registered} 人注册。'.format(
            affiliation=instance.affiliation,
            name=instance.name,
            num_registered=Person.objects.filter(user__isnull=False).count(),
        )
        utils.send_notification(content)
