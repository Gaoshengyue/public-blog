# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-22 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_sitecategory_sitedetaicategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='siteDetaiCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.SiteCategory'),
        ),
    ]
