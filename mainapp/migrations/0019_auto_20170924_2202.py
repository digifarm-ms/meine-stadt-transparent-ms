# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_auto_20170924_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='legal_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
