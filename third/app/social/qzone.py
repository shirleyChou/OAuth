#!/usr/bin/env python
# encoding: utf-8

import re
import json

from .base import OAuth2

QQ_OPENID_PATTERN = re.compile('\{.+\}')

"""
http://wiki.open.qq.com/wiki/website/%E4%BD%BF%E7%94%A8Authorization_Code%E8%8E%B7%E5%8F%96Access_Token
"""

class Qzone(OAuth2):


    def __init__(self):
        # self.login_url = 'https://graph.qq.com/oauth2.0/authorize'
        self.client_id = '101223323'
        self.client_secret = '94be55c133e44072ab0a2b16860e183f'
        self.redirect_uri = 'http://stormy-anchorage-4382.herokuapp.com/account/'
        self.access_token_url = 'https://graph.qq.com/oauth2.0/token'
        self.openid_url = 'https://graph.qq.com/oauth2.0/me'
        self.access_token = None
        self.expires_in = None
        self.uid = None
        self.name = None

    @property
    def authorize_url(self):
        url = super(Qzone, self).authorize_url
        return '%s&state=qzone&which=Login&display=pc' % url

    def get_access_token(self, code):
        super(Qzone, self).get_access_token(code, method='GET', parse=False)


    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
            'oauth_consumer_key': self.client_id,
            'openid': self.uid
        }
        data.update(kwargs)
        return data

    def parse_token(self, res):
        if 'callback(' in res:
            res = res[res.index('(')+1:res.rindex(')')]
            res = json.loads(res)
            # raise SocialAPIError(self.site_name, '', u'%s:%s' % (res['error'],res['error_description']) )
        else:
            res = res.split('&')
            res = [_r.split('=') for _r in res]
            res = dict(res)

        self.access_token = res['access_token']
        self.expires_in = int(res['expires_in'])
        # self.refresh_token = None

        res = self.http_get(self.openid_url, {'access_token': self.access_token}, parse=False)
        res = json.loads(QQ_OPENID_PATTERN.search(res).group())

        self.uid = res['openid']

        _url = 'https://graph.qq.com/user/get_user_info'
        res = self.api_call_get(_url)
        self.name = res['nickname']

        # if res['ret'] != 0:
        #     raise SocialAPIError(self.site_name, _url, res)

        # self.avatar = res['figureurl_qq_1']
        # self.avatar_large = res['figureurl_qq_2']
