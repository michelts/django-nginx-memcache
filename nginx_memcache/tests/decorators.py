import logging
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from nginx_memcache.cache import nginx_cache as cache, get_cache_key
from nginx_memcache.decorators import cache_page_nginx


class CachePageDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_default_args(self):
        def my_view(request):
            return HttpResponse('content')

        # Clear the cache before we do anything.
        request = self.factory.get('/')
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)

        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')

        assert cache.get(cache_key)

    def test_custom_page_version_function(self):
        """
        Asserts that if there is a custom version function, the returned
        version is considered in the cache key.
        """
        def my_view(request):
            return HttpResponse('content')

        # monkey-patch settings to add a custom page version function
        settings.CACHE_NGINX_PAGE_VERSION_FUNCTION = lambda request: 'custom-version'

        request = self.factory.get('/')
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path(), 'custom-version')
        assert not cache.get(cache_key)

        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')

        assert cache.get(cache_key)

        # get back to the original value to not compromise other tests
        settings.CACHE_NGINX_PAGE_VERSION_FUNCTION = None

    def test_custom_encryptation_function(self):
        """
        Asserts that if there is a custom encryptation function, it will be
        used instead of the default md5.
        """
        def my_view(request):
            return HttpResponse('content')

        # monkey-patch settings to add a encryptation function that
        # in this example do nothing
        settings.CACHE_NGINX_ENCRYPTATION_FUNCTION = lambda raw_key: raw_key

        request = self.factory.get('/')
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)

        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')

        assert cache.get(cache_key)

        # get back to the original value to not compromise other tests
        settings.CACHE_NGINX_ENCRYPTATION_FUNCTION = None


class CachePageDecoratorHTTPSTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        settings.CACHE_NGINX_INCLUDE_HTTPS = True

    def test_ssl_requests_can_be_cached(self):

        def my_view(request):
            return HttpResponse('content')

        # Show that is_secure() requests are cached by default
        kwargs = {}
        kwargs["wsgi.url_scheme"] = "https"

        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        logging.info("settings.CACHE_NGINX_INCLUDE_HTTPS should be True, Got: %s" % settings.CACHE_NGINX_INCLUDE_HTTPS)
        logging.info("Trying to cache a view - should be cached")
        logging.info(getattr(settings, 'CACHE_NGINX_INCLUDE_HTTPS', True))
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        assert cache.get(cache_key)

        # Show that HTTPS header requests are cached by default
        kwargs = {}
        kwargs["HTTP_X_FORWARDED_PROTO"] = "HTTPS"
        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        assert cache.get(cache_key)

        kwargs = {}
        kwargs["HTTP_X_FORWARDED_SSL"] = "on"

        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        assert cache.get(cache_key)


class CachePageDecoratorHTTPSSkipCacheTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        ## monkey-patch settings to disable HTTPS cacheing
        settings.CACHE_NGINX_INCLUDE_HTTPS = False

    def test_ssl_requests_can_be_not_cached(self):
        logging.info("settings.CACHE_NGINX_INCLUDE_HTTPS should be False, Got: %s" % settings.CACHE_NGINX_INCLUDE_HTTPS)

        def my_view(request):
            return HttpResponse('content')

        # Show that is_secure requests can *not* be cached cached by default
        kwargs = {}
        kwargs["wsgi.url_scheme"] = "https"

        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        assert not cache.get(cache_key)

        # Show that HTTPS header requests can not be cached cached by default
        kwargs = {}
        kwargs["HTTP_X_FORWARDED_PROTO"] = "HTTPS"
        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        logging.info("Trying to skip cacheing a view - should NOT be cached")
        assert not cache.get(cache_key)

        kwargs = {}
        kwargs["HTTP_X_FORWARDED_SSL"] = "on"

        # Clear the cache before we do anything.
        request = self.factory.get('/', **kwargs)
        cache.clear()
        cache_key = get_cache_key(request.get_host(), request.get_full_path())
        assert not cache.get(cache_key)
        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')
        assert not cache.get(cache_key)
