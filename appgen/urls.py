from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Always go to the appconfig changelist
    (r'^$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/appgen/$', lambda x: HttpResponseRedirect('/admin/appgen/appconfig/')),
    (r'^admin/', include(admin.site.urls)),
)

