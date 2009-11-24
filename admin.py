from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from geoms.models import Geom, GeomRelation

# we could use the default map
#admin.site.register(Geom, GeoModelAdmin)

# Customize the map
class GeomGeoAdmin(GeoModelAdmin):
    options = {
        #'layers': ['google.satellite', 'google.hybrid',  'google.streets' ], # 'google.terrain', ],
        'default_lat': 44,
        'default_lon': -72,
        'default_zoom': 1,
    }
    list_display = [ '__unicode__', 'countries', ]
    prepopulated_fields = { 'slug': ('title',) }

admin.site.register(Geom, GeomGeoAdmin)
admin.site.register(GeomRelation)

