# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CachedPageRecord'
        db.create_table('nginx_memcache_cachedpagerecord', (
            ('base_cache_key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('parent_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('supplementary_identifier', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
        ))
        db.send_create_signal('nginx_memcache', ['CachedPageRecord'])

        # Adding unique constraint on 'CachedPageRecord', fields ['parent_identifier', 'base_cache_key', 'supplementary_identifier']
        db.create_unique('nginx_memcache_cachedpagerecord', ['parent_identifier', 'base_cache_key', 'supplementary_identifier'])


    def backwards(self, orm):
        # Removing unique constraint on 'CachedPageRecord', fields ['parent_identifier', 'base_cache_key', 'supplementary_identifier']
        db.delete_unique('nginx_memcache_cachedpagerecord', ['parent_identifier', 'base_cache_key', 'supplementary_identifier'])

        # Deleting model 'CachedPageRecord'
        db.delete_table('nginx_memcache_cachedpagerecord')


    models = {
        'nginx_memcache.cachedpagerecord': {
            'Meta': {'unique_together': "(('parent_identifier', 'base_cache_key', 'supplementary_identifier'),)", 'object_name': 'CachedPageRecord'},
            'base_cache_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'parent_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'supplementary_identifier': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['nginx_memcache']
