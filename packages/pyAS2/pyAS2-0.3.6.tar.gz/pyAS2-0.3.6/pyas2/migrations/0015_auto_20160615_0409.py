# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-15 04:09
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyas2', '0014_auto_20160420_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='https_ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name='HTTPS Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='certificate',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates'),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='certificate',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates'),
        ),
    ]
