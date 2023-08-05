# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-09 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formly', '0008_auto_20170609_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordinalscale',
            name='kind',
            field=models.CharField(choices=[('likert', 'Likert Scale'), ('rating', 'Rating Scale')], default='likert', max_length=6),
        ),
    ]
