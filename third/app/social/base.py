#!/usr/bin/env python
# encoding: utf-8

from urllib import urlencode, quote
import urllib2
import json
# from functools import wraps


def _http_error_handler(func):
    pass


class OAuth2(object):


    def __init__(self):
        self.login_url = None
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.access_token_url = None
        self.douban_api_url = None

    @property
    def authorize_url(self):
        """return authorize url using for user who login to social website"""
        """ use in the template """
        url = "%s?client_id=%s&response_type=code&redirect_uri=%s" %(
            self.login_url, self.client_id, quote(self.redirect_uri)
        )

        if getattr(self, 'scope', None):
            url = '%s&scope=%s' %(url, '+'.join(self.scope))

        return url

    def http_add_header(self, request):
        pass

    @_http_error_handler
    def http_post(self, url, data, parse=True):
        """return data that contains access_token: data['access_token']"""
        req = urllib2.Request(url, data=urlencode(data))
        self.http_add_header(req)
        data = urllib2.urlopen(req).read()
        if parse:
            return json.loads(data)     # change to json
        return data

    @_http_error_handler
    def http_get(self, url, data, parse=True):
        """return data that contains access_token: data['access_token']"""
        req = urllib2.Request('%s?%s' %(url, urlencode(data)))
        self.http_add_header(req)
        data = urllib2.urlopen(req).read()
        if parse:
            return json.loads(data)     # change to json
        return data

    def get_access_token(self, code, method="POST", parse=True):
        """when user agree to login, the brower would redirect to
        redirect_uri with authorization_code(code='9b73a4248')
        """
        data = {
            'code': code,  #授权码
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code' #必须是这个值
        }

        if method == 'POST':
        	response = self.http_post(self.access_token_url, data, parse=True)
        else:
        	response = self.http_get(self.access_token_url, data, parse=True)
        """
        response = (in douban)
        {
          "access_token":"a14afef0f66fcffce3e0fcd2e34f6ff4",
          "expires_in":3920,
          "refresh_token":"5d633d136b6d56a41829b73a424803ec",
          "douban_user_id":"1221"
        }
        """
        self.parse_token(response)

    def parse_token(self, response):
        """parse data included access_token and user information"""
        raise NotImplementedError()

    def build_api_url(self, url):
        raise NotImplementedError()

    def build_api_data(self, **kwargs):
        raise NotImplementedError()

    def api_call_get(self, url=None, **kwargs):
        url = self.build_api_url(url)
        data = self.build_api_data(**kwargs)
        return self.http_get(url, data)

    def api_call_post(self, url=None, **kwargs):
        url = self.build_api_url(url)
        data = self.build_api_data(**kwargs)
        return self.http_post(url, data)
