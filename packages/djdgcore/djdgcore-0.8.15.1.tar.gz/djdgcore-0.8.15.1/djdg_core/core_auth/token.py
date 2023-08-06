#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/12/14
 """
from __future__ import unicode_literals, absolute_import
from djdg_core.cache.proxy import CacheProxy
from djdg_core import settings
from uuid import uuid1
from djdg_core.core_auth.models import User


token_settings = settings.cache_token_settings


class TokenCache(CacheProxy):
    """
    token在redis中的key
    """
    FORMAT = token_settings['FORMAT']
    KEY_EXPIRE = 7200
    if 'EXPIRE' in token_settings:
        KEY_EXPIRE = token_settings['EXPIRE']

    def __init__(self, token, engine=None):
        super(TokenCache, self).__init__(engine, token=token)
        self.settings = token_settings


def set_token(user_id):
    token = str(uuid1())
    token_cache = TokenCache(token=token)
    token_cache.hook_set(user_id, expire=token_settings.get('EXPIRE', True))
    return token


def get_user_id(token):
    """
    通过token获取user id
    :param token: uuid1 产生的内容
    :return:
    """
    token_cache = TokenCache(token=token)
    user_id, expire_time = token_cache.hook_get(with_ttl=True)
    if not user_id:
        return None
    if token_cache.KEY_EXPIRE:
        interval = token_cache.KEY_EXPIRE >> 1
        if interval > expire_time:
            token_cache.hook_expire(token_cache.KEY_EXPIRE)
    return user_id


def flash_token(token):
    """
    检查token是即将过期
    :param token:
    :return:
    """
    token_cache = TokenCache(token=token)
    if not token_cache.KEY_EXPIRE:
        return False
    expire_time = token_cache.hook_ttl()
    interval = token_cache.KEY_EXPIRE >> 1
    if interval > expire_time:
        token_cache.hook_expire(token_cache.KEY_EXPIRE)
        return True
    return False


def destroy_token(token):
    """
    删除token
    :param token:
    :return:
    """
    token_cache = TokenCache(token=token)
    token_cache.hook_delete()


def get_user_by_token(token):
    user_id = get_user_id(token)
    if not user_id:
        return None
    if settings.USER_MODEL:
        user_model = settings.USER_MODEL['MODEL']
        pk = settings.USER_MODEL.get('PK', 'id')
        user = user_model.objects.get(**{pk: user_id})
        return user
    else:
        return User(token=token)
