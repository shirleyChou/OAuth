from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', 'third.app.login.views.login', name='login'),
    url(r'^auth/', include('third.app.login.urls')),
)
