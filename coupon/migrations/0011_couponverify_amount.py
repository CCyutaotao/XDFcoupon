# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-06 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0010_auto_20170706_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponverify',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
