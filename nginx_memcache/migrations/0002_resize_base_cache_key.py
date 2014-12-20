# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx_memcache', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachedpagerecord',
            name='base_cache_key',
            field=models.CharField(help_text=b'The encrypted result based on the host and path. This will be combined with any prefix and the version to get the real cache key stored in memcache', max_length=255, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
