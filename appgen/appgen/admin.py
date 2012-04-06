from django.contrib.gis import admin
from appgen.models import *
from appgen.forms import AppConfigForm

admin.site.register(UserFeature)
admin.site.register(BaseKml)

class AppGeoModelAdmin(admin.OSMGeoAdmin): 
    form = AppConfigForm
    list_display = ('app', 'wms', 'links', 'status', 'desc', 'data_list', 'command_html') # command_html must be last!


admin.site.register(AppConfig, AppGeoModelAdmin)
