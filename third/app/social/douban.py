#!/usr/bin/env python
# encoding: utf-8

from base import OAuth2

"""
http://developers.douban.com/wiki/?title=oauth2
"""


class DouBan(OAuth2):

    def __init__(self):
        self.login_url = 'https://www.douban.com/service/auth2/auth'
        self.client_id = '0e2cb973302b699d2a862c5990823cd7'
        self.client_secret = '5a2a7988dcaee9ef'
        self.redirect_uri = 'https://vast-hamlet-2195.herokuapp.com/account/'
        self.access_token_url = 'https://www.douban.com/service/auth2/token'
        self.douban_api_url = 'https://api.douban.com'
        self.uid = None
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None
        self.name = None
        # self.avatar = None

    @property
    def authorize_url(self):
        url = super(DouBan, self).authorize_url
        return '%s&state=douban' % url

    def build_api_url(self, url):
        return '%s%s' %(self.douban_api_url, url)

    def build_api_data(self, **kwargs):
        return kwargs

    def http_add_header(self, request):
        if getattr(self, 'access_token', None):
            request.add_header('Authorization',
                               'Bearer %s' % self.access_token)

    def parse_token(self, res):
        self.uid = res['douban_user_id']
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']

        res = self.api_call_get('/v2/user/~me')

        self.name = res['name']
        # self.avatar = res['avatar']
        # self.avatar_large = ""
