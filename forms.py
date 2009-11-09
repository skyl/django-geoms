from django import forms
from olwidget.widgets import EditableMap
from geoms.models import Geom

class GeomForm(forms.ModelForm):
    #point = forms.CharField(widget=EditableMap())
    #mpoint = forms.CharField(widget=EditableMap())
    #line = forms.CharField(widget=EditableMap())
    #mline = forms.CharField(widget=EditableMap())
    #poly = forms.CharField(widget=EditableMap())
    #mpoly = forms.CharField(widget=EditableMap())
    collection = forms.CharField(widget=EditableMap(
        options = {
            'geometry': ['point','linestring', 'polygon'],
            'is_collection': True,
        }
    ))

    class Meta:
        model = Geom
        fields = ('collection',)

class PointForm(forms.ModelForm):

    class Meta:
        model = Geom
        fields = ('title', 'point' )

    '''
    class Media:
        css = {
                'all': (
                    'points/css/points.css',
                    'points/css/jq-ui.css',
                )
        }

        js = ('points/js/points.js',)
    '''

