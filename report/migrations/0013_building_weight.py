# Generated by Django 3.0.3 on 2020-03-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0012_building_uuid_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='权重'),
        ),
    ]