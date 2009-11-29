"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from geoms.models import Geom

class TestGeomData(TestCase):

    fixtures = ['each-field.json',]

    def test_count(self):
        assert len(Geom.objects.all()) == 7

    def test_views(self):
        c = Client()
        response = c.get( reverse('geoms_list') )
        self.failUnlessEqual( response.status_code, 200 )

        response = c.get( reverse('geoms_detail',
                kwargs={ 'id':1 } )
        )
        self.failUnlessEqual( response.status_code, 200 )


__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.


"""}
