# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_tus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='uploaded_file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='uploaded'),
        ),
    ]
