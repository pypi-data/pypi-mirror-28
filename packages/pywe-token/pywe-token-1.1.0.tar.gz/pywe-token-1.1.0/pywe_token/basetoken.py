# -*- coding: utf-8 -*-

import time

from pywe_base import BaseWechat
from pywe_storage import MemoryStorage


class BaseToken(BaseWechat):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(BaseToken, self).__init__()
        self.appid = appid
        self.secret = secret
        self.token = token
        self.storage = storage or MemoryStorage()

        if self.token:
            expires_in = 7200
            access_info = {
                'access_token': self.token,
                'expires_in': expires_in,
                'expires_at': int(time.time()) + expires_in,
            }
            self.storage.set(self.access_info_key, access_info, expires_in)

    @property
    def access_info_key(self):
        return '{0}:access:info'.format(self.appid)

    def update_params(self, appid=None, secret=None, token=None, storage=None):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.token = token or self.token
        self.storage = storage or self.storage
