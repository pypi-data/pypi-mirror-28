# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_page_page_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='num_bundle_elements',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Cantidad de elementos para el pack', choices=[(4, b'4'), (6, b'6')]),
            preserve_default=True,
        ),
    ]
