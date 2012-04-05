from django.contrib.gis import admin
from appgen.models import *
from appgen.forms import AppConfigForm

admin.site.register(UserFeature)
admin.site.register(BaseKml)
admin.site.register(AppConfig, admin.GeoModelAdmin)
