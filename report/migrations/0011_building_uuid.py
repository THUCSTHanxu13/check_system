# Generated by Django 3.0.3 on 2020-03-11 00:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0010_record_is_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='code',
        ),
        migrations.AddField(
            model_name='building',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='内部编码'),
        ),
    ]