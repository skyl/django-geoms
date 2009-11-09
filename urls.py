from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
    url(r'^$', view='mpolys.views.list', name="mpolys_list"),
    url(r'^(?P<id>\d+)/$', view='mpolys.views.detail', name='mpolys_detail'),

    url(r'^delete/(?P<id>\d+)/', view='mpolys.views.delete', name='mpolys_delete'),

    url(r'change/(?P<id>\d+)/', view='mpolys.views.change', name='mpolys_change'),


    url(r'list/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='mpolys.views.list', name='mpolys_list'),

    url(r'list/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/$',\
            view='mpolys.views.list', name='mpolys_list'),

    url(r'add/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='mpolys.views.add', name='mpolys_add'),

)


'''
from settings import INSTALLED_APPS

if 'piston' in INSTALLED_APPS:
    from piston.resource import Resource
    from piston.authentication import HttpBasicAuthentication

    from mpolys.handlers import PointHandler

    point_resource = Resource(handler=PointHandler)

    urlpatterns += patterns('',

            url(r'^api/(?P<id>\d+)/$', point_resource),

    )

'''
