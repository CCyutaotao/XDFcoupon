# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-06 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0009_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discounttype',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userlist',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]
