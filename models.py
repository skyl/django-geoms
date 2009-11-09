from django.db.models import Q
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# check if different apps are installed
from django.conf import settings
if "world" in settings.INSTALLED_APPS:
    from world.models import WorldBorders
else:
    WorldBorders = None

if "django.contrib.auth" in settings.INSTALLED_APPS:
    from django.contrib.auth.models import User
else:
    User = None

if 'tagging' in settings.INSTALLED_APPS:
    from tagging.fields import TagField
else:
    TagField = None


class Geom(models.Model):
    ''' a geographic geom that can be added to any model instance

    '''
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    datetime = models.DateTimeField(editable=False, auto_now=True)

    if User:
        owner = models.ForeignKey(User, blank=True, null=True)

    if TagField:
        tags = TagField()

    point = models.PointField(blank=True, null=True)
    mpoint = models.MultiPointField(blank=True, null=True)
    line = models.LineStringField(blank=True, null=True)
    mline = models.MultiLineStringField(blank=True, null=True)
    poly = models.PolygonField(blank=True, null=True)
    mpoly = models.MultiPolygonField(blank=True, null=True)
    collection = models.GeometryCollectionField(blank=True, null=True)

    zoom = models.PositiveIntegerField(blank=True, null=True)
    objects = models.GeoManager()

    def countries(self):
        if WorldBorders:
            geoms = [self.point, self.mpoint, self.line, self.mline, self.poly,
                    self.mpoly]
            if self.collection:
                geoms.extend([g for g in self.collection])
            q = Q()
            for g in geoms:
                if g is not None:
                    q =     q|Q(mpoly__intersects=g)

            if q:
                return WorldBorders.objects.filter(q)
            else:
                return None

        else:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('geoms.views.detail', (), {'id':self.id,} )

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        ordering = ( '-datetime', )


class GeomRelation(models.Model):
    ''' For tagging many objects to a Geom object and vice-versa '''

    geom = models.ForeignKey(Geom)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    objects = models.GeoManager()


def get_geoms_for_object(obj):
    ''' takes an object and returns qs of related Geoms.

    '''
    ct = ContentType.objects.get_for_model(obj)
    id = obj.id
    grs = GeomRelation.objects.filter( content_type=ct, object_id=id )
    return Geom.objects.filter(geomrelation__in=grs)

def get_objects_for_geom(geom):
    ''' takes a geom and returns the related objects '''
    pass


