from django.conf.urls import patterns, url

urlpatterns = patterns('third.app.login.views',
    # url(r'^$', 'login', name='login'),
    url(r'^login/$', 'login', name = 'login'),
    url(r'^register/$', 'register', name = 'regist'),
    url(r'^index/$', 'index', name = 'index'),
)
