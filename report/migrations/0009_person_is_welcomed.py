# Generated by Django 3.0.3 on 2020-03-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_default_false'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_welcomed',
            field=models.BooleanField(default=False, verbose_name='发送欢迎消息'),
        ),
    ]