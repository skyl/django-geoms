from django.http import HttpResponseRedirect, HttpResponse,\
        HttpResponseNotFound
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType


from geoms.forms import GeomForm
from geoms.models import Geom
from olwidget.widgets import MapDisplay


#from vectorformats.Formats import Django, GeoJSON
from django.core import serializers


def list(request, app_label=None, model_name=None, id=None, ):
    ''' List all geoms (ALL, all for model instance, or all for table)

    '''

    # FIXME, I think this could be DRYed out a bit; experimental overloading of the
    # view might not be the coolest thing.
    if not id and not model_name and not app_label:
        geoms = Geom.objects.all()[:15]
        f = []
        for g in geoms:
            if g.point:
                f.append(g.point)
            if g.line:
                f.append(g.line)
            if g.poly:
                f.append(g.poly)
            if g.mpoint:
                f.extend(g.mpoint)
            if g.mline:
                f.extend(g.mline)
            if g.mpoly:
                f.extend(g.mpoly)
            if g.collection:
                f.extend(g.collection)


        map = MapDisplay( fields=f,
                    options = {
                        'map_style':{'width':'100%', 'height':'550px',},
                        'layers': ['google.satellite', 'google.hybrid',  'google.streets' ], # 'google.terrain', ],
                        'default_lat': 44,
                        'default_lon': -72,
                        'default_zoom': 1,
                        'map_div_class':'',
                        'map_div_style': {'width':'100%',},
                    }
        )

        context = { 'map':map,'geoms':geoms, }
        return render_to_response('geoms/all.html', context,\
                context_instance=RequestContext(request))

    elif id and model_name and app_label:
        try:
            ct = ContentType.objects.get(\
                    app_label = app_label,
                    model = model_name)
            obj = ct.get_object_for_this_type( id=id )

        except:
            return HttpResponseRedirect(reverse('geoms_list'))


        geoms = Geom.objects.filter( content_type=ct, object_id=id )
        map = MapDisplay( fields=[p.point for p in geoms],
                map_options = {
                    'map_style':{'width':'100%', 'height':'550px',},
                }
        )

        context = {'geoms':geoms, 'object':obj, 'content_type':ct, 'map':map, }
        return render_to_response('geoms/all.html', context,\
                context_instance=RequestContext(request))

    elif app_label and model_name and not id:
        try:
            ct = ContentType.objects.get(\
                    app_label = app_label,
                    model = model_name)

        except:
            return HttpResponseRedirect(reverse('geoms_list'))

        geoms = Geom.objects.filter(content_type = ct)
        map = MapDisplay( fields=[p.point for p in geoms],
                map_options = {
                    'map_style':{'width':'100%', 'height':'550px',},
                }
        )
        context = {'geoms':geoms, 'content_type':ct, 'map':map,}

        return render_to_response('geoms/all.html', context,\
                context_instance=RequestContext(request))

    else:
        return HttpResponseNotFound()

def detail(request, id):
    ''' Responds with the point and related object information

    '''

    try:
        point = Geom.objects.get( id=id )

    except:
        return HttpResponseRedirect(reverse('geoms_list'))


    map = MapDisplay( fields = [ point.point, ],
            map_options = {
                    'map_style':{'width':'100%', 'height':'550px',},
            }
    )

    ct = ContentType.objects.get(\
            app_label = point.content_type.app_label,
            model = point.content_type.model)

    obj = ct.get_object_for_this_type(id = point.object_id)

    context = {'point':point, 'object':obj, 'content_type': ct, 'map':map,  }

    return render_to_response('geoms/detail.html', context,\
                context_instance=RequestContext(request))

@login_required
def delete(request, id):
    ''' can delete a point with a POST from the owner

    '''
    try:
        point = Geom.objects.get(id=id)
    except:
        return HttpResponseNotFound()

    context = {'point':point,}
    if request.user == point.owner:

        if request.method == 'POST':
            point.delete()
            return HttpResponseNotFound()

        else:
            return render_to_response('geoms/confirm_delete.html', context,\
                    context_instance=RequestContext(request))

    else:
        return HttpResponseNotFound()

@login_required
def change(request, id):
    ''' Change the data for a single Geom() obj '''

    try:
        point = Geom.objects.get(id=id)
    except:
        return HttpResponseNotFound()

    if request.method == 'POST' and point.owner == request.user:

        form = GeomForm(request.POST, instance=point)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(point.get_absolute_url())

    elif point.owner == request.user:
        form = GeomForm( instance=point)
        context = {'point':point, 'form':form, }
        return render_to_response('geoms/change.html', context,\
                context_instance=RequestContext(request) )

    else:
        return HttpResponseNotFound()

@login_required
def add(request, app_label, model_name, id):
    '''add a point to a content_object

    POST the point and the zoom.  The owner is request.user and the related
    obj is received from the url.
    '''
    try:
        ct = ContentType.objects.get(\
                app_label = app_label,
                model = model_name)
        obj = ct.get_object_for_this_type( id=id )

    except:
        return HttpResponseNotFound()

    if request.method == 'POST':
        request.POST.update( {'owner':request.user.id, 'object_id':id,\
                'content_type':ct.id, 'content_obj':obj,} )
        form = GeomForm(request.POST)

        if form.is_valid():
            form.save()

            #try:
            #    return HttpResponseRedirect(request.META['HTTP_REFERER'])

            #except:

            try:
                return HttpResponseRedirect(obj.get_absolute_url())

            except:
                return HttpResponseRedirect(reverse('geoms_list'))

    else:
        form = GeomForm()

    context = {'form':form, 'object':obj, 'content_type':ct, }
    context.update(locals())

    return render_to_response('geoms/add.html', context,\
            context_instance = RequestContext(request))


