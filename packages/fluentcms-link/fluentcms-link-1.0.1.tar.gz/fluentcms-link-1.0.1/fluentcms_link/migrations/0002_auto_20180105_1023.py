# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-05 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('fluentcms_link', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='linkitem',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='linkitem',
            name='mailto',
            field=models.EmailField(blank=True, help_text='An email adress has priority over a text or page link.', max_length=254, null=True, verbose_name='mailto'),
        ),
    ]
