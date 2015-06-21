from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('third.app.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login'),
    # url(r'^account/$', 'social_data', name='personal_account'),
    url(r'^account/\?code=(?P<code>\w+)&state=(?P<state>\w+)$', 'handle_data', name='return code'),
    url(r'^account/\?state=(?P<state>\w+)&code=(?P<code>\w+)$', 'handle_data', name='code return'),

    url(r'^account/bind_oauth/qzone/', 'bind_qzone'),
    url(r'^account/bind_oauth/weibo/', 'bind_weibo'),
    url(r'^account/bind_oauth/douban/', 'bind_douban'),

    url(r'^account/cancel_oauth/qzone/', 'cancel_qzone'),
    url(r'^account/cancel_oauth/weibo/', 'cancel_weibo'),
    url(r'^account/cancel_oauth/douban/', 'cancel_douban'),

    url(r'^auth/logout/$', 'logout', name='social_logout'),
)

# weibo return
# http://stormy-anchorage-4382.herokuapp.com/account/?state=weibo&code=e77a11d30d62ac7bab10932e47bfcde5

# douban return
# http://stormy-anchorage-4382.herokuapp.com/account/?code=cad7b4da5b86b0f8&state=douban

# tecent teturn
# http://stormy-anchorage-4382.herokuapp.com/account/?code=5AD5DE9AA8769119D945EB2EB41C0408&state=qzone


