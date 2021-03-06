from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
    url(r'^$', view='geoms.views.list', name="geoms_list"),
    url(r'^(?P<id>\d+)/$', view='geoms.views.detail', name='geoms_detail'),

    url(r'^delete/(?P<id>\d+)/', view='geoms.views.delete', name='geoms_delete'),

    url(r'change/(?P<id>\d+)/', view='geoms.views.change', name='geoms_change'),


    url(r'list/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='geoms.views.list', name='geoms_list'),

    url(r'list/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/$',\
            view='geoms.views.list', name='geoms_list'),

    url(r'add/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='geoms.views.add', name='geoms_add'),

)

from django.conf import settings

if 'piston' in settings.INSTALLED_APPS:
    from piston.resource import Resource
    from piston.authentication import OAuthAuthentication

    from geoms.handlers import GeomHandler

    auth = OAuthAuthentication()
    ad = { 'authentication': auth }
    geom_resource = Resource( handler=GeomHandler, **ad)

    urlpatterns += patterns('',
            url(r'^api/(?P<id>\d+)/$', geom_resource),
    )

