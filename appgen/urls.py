from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Always go to the appconfig changelist
    url(r'^activate/(?P<pk>\d+)/$', 'appgen.views.activate', name='activate'),
    url(r'^initialize/(?P<pk>\d+)/$', 'appgen.views.initialize', name='initialize'),
    url(r'^delete/(?P<pk>\d+)/$', 'appgen.views.delete', name='delete'),
    url(r'^initial_docs/$', 'appgen.views.initial_docs', name='initial_docs'),
    (r'^$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/appgen/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/', include(admin.site.urls)),
)

