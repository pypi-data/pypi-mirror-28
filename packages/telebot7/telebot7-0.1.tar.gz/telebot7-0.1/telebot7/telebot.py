#!/usr/bin/env python3
# coding: utf8


from functools import partial

import requests


class TeleBot(object):

    def __init__(self, access_token):
        self._access_token = access_token

    def __getattr__(self, method):
        return partial(self._call, method)

    def __call__(self, method, **params):
        return getattr(self, method)(**params)

    def _call(self, method, **params):
        url = 'https://api.telegram.org/bot{}/{}'.format(self._access_token, method)
        return requests.post(url, params).json()

    def getUpdates(self, **params):
        url = 'https://api.telegram.org/bot{}/{}'.format(self._access_token, 'getUpdates')
        if 'timeout' in params:
            return requests.post(url, params, timeout=params['timeout']+5).json()
        return requests.post(url, params).json()
