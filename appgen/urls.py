from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Always go to the appconfig changelist
    url(r'^load/(?P<pk>\d+)/$', 'appgen.views.load', name='load'),
    url(r'^active/$', 'appgen.views.active', name='active'),
    (r'^$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/appgen/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/', include(admin.site.urls)),
)

