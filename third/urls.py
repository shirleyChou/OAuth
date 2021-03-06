from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('third.app.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login'),

    url(r'^account/$', 'handle_data'),
    url(r'^account/bind/$', 'show_result'),
    url(r'^account/cancel_oauth/qzone/', 'cancel_qzone'),
    url(r'^account/cancel_oauth/weibo/', 'cancel_weibo'),
    url(r'^account/cancel_oauth/douban/', 'cancel_douban'),
    url(r'^account/delete_account/', 'delete_account'),

    url(r'^auth/logout/$', 'logout'),
)
