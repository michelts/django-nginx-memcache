from django.apps import AppConfig


class NginxMemcacheConfig(AppConfig):
    name = 'nginx_memcache'
    verbose_name = 'Nginx Memcache'

    def ready(self):
        from nginx_memcache.signals import (  # noqa
            handle_single_page_invalidation,
            handle_multiple_page_invalidation,
        )
