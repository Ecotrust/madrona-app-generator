from django.contrib.gis import admin
from appgen.models import *
from appgen.forms import AppConfigForm

admin.site.register(UserFeature)
admin.site.register(BaseKml)

class AppGeoModelAdmin(admin.OSMGeoAdmin): 
    form = AppConfigForm
    list_display = ('app', 'desc', 'features_list', 'wms', 'links', 'status', 'command_html')


admin.site.register(AppConfig, AppGeoModelAdmin)
