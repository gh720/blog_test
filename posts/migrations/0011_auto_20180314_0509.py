# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-14 00:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20180314_0509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('view_post', 'Can view entry')]},
        ),
    ]
