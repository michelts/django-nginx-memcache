default_app_config = 'nginx_memcache.apps.NginxMemcacheConfig'


VERSION = (0, 2, 4,)


def get_version():
    version = '%s.%s.%s' % (
        VERSION[0],
        VERSION[1],
        VERSION[2]
    )
    try:
        version = '%s.%s.%s %s' % (
            VERSION[0],
            VERSION[1],
            VERSION[2],
            VERSION[3]
        )
    except IndexError:
        pass
    return version
