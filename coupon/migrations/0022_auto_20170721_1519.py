# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-21 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0021_auto_20170721_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlist',
            name='duty',
            field=models.CharField(choices=[('\u5458\u5de5', '\u5458\u5de5'), ('\u90e8\u95e8\u603b\u76d1', '\u90e8\u95e8\u603b\u76d1'), ('\u5e02\u573a\u603b\u76d1', '\u5e02\u573a\u603b\u76d1'), ('\u5ba2\u670d\u603b\u76d1', '\u5ba2\u670d\u603b\u76d1'), ('\u6821\u957f', '\u6821\u957f')], default='\u666e\u901a\u804c\u5458', max_length=20),
        ),
    ]
