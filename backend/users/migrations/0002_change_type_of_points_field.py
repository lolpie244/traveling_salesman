# Generated by Django 4.1.3 on 2022-11-22 23:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_create_history_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='path'
        ),
        migrations.AddField(
            model_name='history',
            name='path',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None),
        ),
        migrations.RemoveField(
            model_name='history',
            name='points'
        ),
        migrations.AddField(
            model_name='history',
            name='points',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None),
        ),
    ]