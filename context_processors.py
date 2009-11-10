from geoms.forms import GeomForm

form = GeomForm()

def geom_media(request):
    '''provides the media for an olwidget for maps data being dyn-ajax

    '''
    #string = form.media.render()
    from django.conf import settings
    GAK = settings.GOOGLE_API_KEY

    return {
            #'geom_form_media': string,
            'GAK': GAK
    }

