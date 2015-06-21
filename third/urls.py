from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('third.app.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login'),

    # url(r'^account/\?code=(?P<code>\w+)&state=(?P<state>\w+)', 'handle_data'),
    # url(r'^account/\?state=(?P<state>\w+)&code=(?P<code>\w+)', 'handle_data'),

    url(r'^account/$', 'handle_data'),
    
    # url(r'^account/bind_oauth/qzone/', 'bind_qzone'),
    # url(r'^account/bind_oauth/weibo/', 'bind_weibo'),
    # url(r'^account/bind_oauth/douban/', 'bind_douban'),

    url(r'^account/cancel_oauth/qzone/', 'cancel_qzone'),
    url(r'^account/cancel_oauth/weibo/', 'cancel_weibo'),
    url(r'^account/cancel_oauth/douban/', 'cancel_douban'),

    url(r'^auth/logout/$', 'logout', name='social_logout'),
)
