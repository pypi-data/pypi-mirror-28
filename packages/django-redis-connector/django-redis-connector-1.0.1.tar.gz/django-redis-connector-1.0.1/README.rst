======================
django-redis-connector
======================

Django Redis Connector

Installation
============

::

    pip install django-redis-connector


Usage
=====

::

    from django_redis_connector import connector

    # Redis 设置
    REDIS = {
        'default': {
            'HOST': '127.0.0.1',
            'PORT': 6379,
            'USER': '',
            'PASSWORD': '',
            'db': 0,
        }
    }

    # Redis 连接
    REDIS_CACHE = connector(REDIS.get('default', {}))

