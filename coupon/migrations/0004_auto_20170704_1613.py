# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-04 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_auto_20170704_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='gradeindex',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]