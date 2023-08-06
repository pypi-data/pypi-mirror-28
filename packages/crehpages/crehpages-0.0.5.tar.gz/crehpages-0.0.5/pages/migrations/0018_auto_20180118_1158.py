# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20171219_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='product_categories',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='video_provider',
            field=models.CharField(blank=True, max_length=200, null=True, choices=[(b'Wistia', b'Wistia'), (b'Vimeo', b'Vimeo')]),
            preserve_default=True,
        ),
    ]
