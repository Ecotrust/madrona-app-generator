from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Always go to the appconfig changelist
    url(r'^activate/(?P<pk>\d+)/$', 'appgen.views.activate', name='activate'),
    url(r'^initialize/(?P<pk>\d+)/$', 'appgen.views.initialize', name='initialize'),
    (r'^$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/appgen/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/', include(admin.site.urls)),
)

