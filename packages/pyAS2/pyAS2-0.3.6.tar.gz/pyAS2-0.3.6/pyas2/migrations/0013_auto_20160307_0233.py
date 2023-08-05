# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-07 02:33
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyas2', '0012_auto_20151006_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='as2_name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='AS2 Identifier'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Organization Name'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='https_ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name='HTTPS Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='certificate',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates'),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='certificate',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates'),
        ),
    ]
