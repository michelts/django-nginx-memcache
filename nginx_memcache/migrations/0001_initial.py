# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CachedPageRecord',
            fields=[
                ('base_cache_key', models.CharField(help_text=b'The encrypted result based on the host and path. This will be combined with any prefix and the version to get the real cache key stored in memcache', max_length=32, serialize=False, primary_key=True)),
                ('parent_identifier', models.CharField(help_text=b'A 255-char identifier for whatever your parent object is.Could be a slug, a subdomain, or a Site ID [as a string]. If no lookup_identifier is passed to the cache decorator, this value will be the hostname of the server (which is fine).', max_length=255, db_index=True)),
                ('supplementary_identifier', models.CharField(help_text=b"Additional meta string you can use to scope your invalidation calls to a subset of keys - eg 'news' or 'category_3'. 45 chars max.", max_length=45, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cachedpagerecord',
            unique_together=set([('parent_identifier', 'base_cache_key', 'supplementary_identifier')]),
        ),
    ]
