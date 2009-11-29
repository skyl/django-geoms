from django.contrib.auth.decorators import login_required
import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from geoms.models import Geom
from geoms.forms import GeomForm

class AnonGeomHandler(BaseHandler):
    allowed_methods = ('GET', )
    fields = ('title', 'datetime',
                    'point', 'mpoint',
                    'line', 'mline',
                    'poly', 'mpoly',
                    'collection', 'zoom',
                    'owner', 'tags', 'slug')
    model = Geom

    def read(self, request, id):
        geom = Geom.objects.get( id=int(id) )
        return geom


class GeomHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('title', 'datetime',
                    'point', 'mpoint',
                    'line', 'mline',
                    'poly', 'mpoly',
                    'collection', 'zoom',
                    'owner', 'tags', 'slug')
    #exclude = ('id', re.compile(r'^private_'))
    model = Geom
    anonymous = AnonGeomHandler

    def read(self, request, id):
        geom = Geom.objects.get( id=int(id) )
        return geom


    def update(self, request, id):

        geom = Geom.objects.get( id=int(id) )
        if not request.user == geom.owner:
            return rc.FORBIDDEN

        geom.title = request.PUT.get('title')
        geom.save()

        return geom

    '''
    def create(self, request):
        p = PointForm(request.POST)
        p.save()
    '''

    def delete(self, request, id):

        geom = Geom.objects.get( id=int(id) )

        if not request.user == geom.owner:
            return rc.FORBIDDEN # returns HTTP 401

        geom.delete()

        return rc.DELETED # returns HTTP 204


