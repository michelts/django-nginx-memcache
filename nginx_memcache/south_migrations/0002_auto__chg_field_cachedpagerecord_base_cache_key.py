# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CachedPageRecord.base_cache_key'
        db.alter_column('nginx_memcache_cachedpagerecord', 'base_cache_key', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True))

    def backwards(self, orm):

        # Changing field 'CachedPageRecord.base_cache_key'
        db.alter_column('nginx_memcache_cachedpagerecord', 'base_cache_key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True))

    models = {
        'nginx_memcache.cachedpagerecord': {
            'Meta': {'unique_together': "(('parent_identifier', 'base_cache_key', 'supplementary_identifier'),)", 'object_name': 'CachedPageRecord'},
            'base_cache_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'parent_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'supplementary_identifier': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['nginx_memcache']
