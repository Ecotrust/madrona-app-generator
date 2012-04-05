from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'appgen.views.main', name='main'),
)

from django.contrib import admin
admin.autodiscover()
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

