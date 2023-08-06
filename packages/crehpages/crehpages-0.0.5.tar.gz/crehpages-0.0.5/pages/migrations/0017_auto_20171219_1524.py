# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_page_num_bundle_elements'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='video_hash',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='video_provider',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='num_bundle_elements',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Quantity of elements for the bundle', choices=[(4, b'4'), (6, b'6')]),
            preserve_default=True,
        ),
    ]
