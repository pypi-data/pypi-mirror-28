# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, null=True)),
                ('created_at', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(auto_now=True)),
                ('model_name', models.CharField(max_length=200)),
                ('model_uuid', models.CharField(max_length=200)),
                ('model_id', models.IntegerField()),
                ('command', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=200)),
                ('intial_payload', models.TextField()),
                ('status', models.IntegerField(choices=[(0, b'completed'), (1, b'pending'), (2, b'running'), (3, b'PROCESSING'), (-1, b'error'), (-2, b'error_timeout'), (-3, b'error_processing')], default=1)),
                ('response_payload', models.TextField(blank=True, null=True)),
                ('error_notes', models.TextField(blank=True, null=True)),
                ('job_timeout', models.IntegerField(default=3600)),
                ('timeout_at', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(blank=True, null=True)),
                ('job_type', models.CharField(choices=[(b'synchronous', b'synchronous'), (b'local', b'local'), (b'asynchronous', b'asynchronous')], default=b'local', max_length=200)),
                ('run_at', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(blank=True, null=True)),
                ('response_at', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(blank=True, null=True)),
                ('completed_at', django_framework.django_helpers.model_helpers.model_fields.unix_epoch_date_time_field.UnixEpochDateTimeField(blank=True, null=True)),
            ],
        ),
    ]
