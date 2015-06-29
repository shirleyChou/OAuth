#!/usr/bin/env python
# encoding: utf-8

from base import OAuth2

"""
http://open.weibo.com/wiki/
%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E
"""


class WeiBo(OAuth2):

    def __init__(self):
        self.login_url = 'https://api.weibo.com/oauth2/authorize'
        self.client_id = '2699499178'
        self.client_secret = '37b2c55e6cdbed4b9c35ad2b4abfe8b6'
        self.redirect_uri = 'https://vast-hamlet-2195.herokuapp.com/account/'
        self.access_token_url = 'https://api.weibo.com/oauth2/access_token'
        self.access_token = None
        self.expires_in = None
        self.uid = None
        self.name = None

    @property
    def authorize_url(self):
        url = super(WeiBo, self).authorize_url
        return '%s&state=weibo' % url

    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {'access_token': self.access_token}
        data.update(kwargs)
        return data

    def parse_token(self, res):
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        # self.remind_in = res['remind_in']
        self.uid = res['uid']

        res = self.api_call_get(
            'https://api.weibo.com/2/users/show.json',
            uid=self.uid)

        self.name = res['name']
        # self.avatar = res['avatar']
        # self.avatar = res['profile_image_url']
        # self.avatar_large = res['avatar_large']

    # def post_status(self, text):
    # 	if isinstance(text, unicode):
    # 		text = text.encode('utf8')

    # 	url = 'https://api.weibo.com/2/statuses/update.json'
    # 	res = self.api_call_post(url, status=text)
