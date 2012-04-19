from django.contrib.gis import admin
from appgen.models import *
from appgen.forms import AppConfigForm

admin.site.register(UserFeature)
admin.site.register(BaseKml)

class WorldGeoAdmin(admin.OSMGeoAdmin):
    default_lon = 0
    default_lat = 0 
    default_zoom = 1
    map_width = 600
    map_height = 400

class AppGeoModelAdmin(WorldGeoAdmin): 
    form = AppConfigForm
    list_display = ('app', 'wms', 'links', 'status', 'desc', 'data_list', 'command_html') # command_html must be last!

admin.site.register(AppConfig, AppGeoModelAdmin)
