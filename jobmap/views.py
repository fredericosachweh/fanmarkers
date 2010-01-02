from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.db.models import Q


from company.models import Company
from operation.models import OpBase, Operation
from position.models import Position, Status
from airport.models import Airport
 
@render_to('view_jobmap.html')
def jobmap(request):

    usa_bases = OpBase.objects.filter(base__country__exact="US")
    alaska_bases = usa_bases.filter(base__region__name__exact="AK")
    russia_bases = OpBase.objects.filter(base__country__exact="RU")
    india_bases = OpBase.objects.filter(base__country__exact="IN")
    canada_bases = OpBase.objects.filter(base__country__exact="CA")

    usa_h = Status.objects.filter(   Q(assign_bases__in=usa_bases) | Q(choice_bases__in=usa_bases)    ).distinct().count()
    usa_t = Position.objects.filter( operation__opbase__in=usa_bases ).distinct().count()

    canada_h = Status.objects.filter(   Q(assign_bases__in=canada_bases) | Q(choice_bases__in=canada_bases)    ).distinct().count()
    canada_t = Position.objects.filter( operation__opbase__in=canada_bases ).distinct().count()

    india_h = Status.objects.filter(   Q(assign_bases__in=india_bases) | Q(choice_bases__in=india_bases)    ).distinct().count()
    india_t = Position.objects.filter( operation__opbase__in=india_bases ).distinct().count()

    russia_h = Status.objects.filter(   Q(assign_bases__in=russia_bases) | Q(choice_bases__in=russia_bases)    ).distinct().count()
    russia_t = Position.objects.filter( operation__opbase__in=russia_bases ).distinct().count()

    alaska_h = Status.objects.filter(   Q(assign_bases__in=alaska_bases) | Q(choice_bases__in=alaska_bases)    ).distinct().count()
    alaska_t = Position.objects.filter( operation__opbase__in=alaska_bases ).distinct().count()

    return locals()

@render_to('view_jobmap.html')
def jobmap(request):
    from django.db.models import Q

    INDIA =       ['IN','LK']
    AUSTRALIA =   ['AU','NZ','NC','VU','FJ','AS','TO','TV','TK','WF','CK','NU','PF']
    M_EAST =      ['AE','AM','AF','BH','IR','IQ','IL','JO','KW','LB','YE','SY','OM','QA','PK', 'SA']
    E_EUROPE =    ['TR','GR','HU','MD','PL','BY','SK','CZ','RO','HR','BA','AL','MK','ME','CY','SI','LT','LV','EE']
    INDONESIA =   ['ID','PG','SG','MY','PH']
    SCANDANAVIA = ['IS','NO','SE','FI']
    CHINA =       ['KP','KR','MN','HK','MO']
    EUROPE =      ['FR','UK','IT','DK','DE','IE', 'PT','ES','LU','AD','VA','SM','IM','','']
    RUSSIA =      ['RU','','',]
    CARRIBEAN =   ['AG','AI','AN','AW','BB','BL','BM','BS','CU','DM','DO','GD','GP','HT','JM','KN','KY','LC','MF','MQ','MS','PM','PR','TC','TT','VC','VG','VI']
    AMERICAS =    ['MX','SV','PA','NI','HN','BZ','GT','CR']


    africa_h = Status.objects.filter(  Q(assign_bases__base__country__continent='AF') | Q(choice_bases__base__country__continent='AF') ).distinct().count()
    africa_t = Position.objects.filter(  operation__opbase__base__country__continent='AF' ).distinct().count()

    usa_h = Status.objects.filter(  Q(assign_bases__base__country__code='US') | Q(choice_bases__base__country__code='US') ).distinct().count()
    usa_t = Position.objects.filter(  operation__opbase__base__country__code='US').distinct().count()

    alaska_h = Status.objects.filter(  Q(assign_bases__base__region__code='US-AK') | Q(choice_bases__base__region__code='US-AK') ).distinct().count()

    alaska_t = Position.objects.filter(  operation__opbase__base__region__code='US-AK').distinct().count()

    india_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=INDIA) | Q(choice_bases__base__country__code__in=INDIA) ).distinct().count()

    india_t = Position.objects.filter(  operation__opbase__base__country__code__in=INDIA).distinct().count()

    australia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=AUSTRALIA) | Q(choice_bases__base__country__code__in=AUSTRALIA) ).distinct().count()

    australia_t = Position.objects.filter(  operation__opbase__base__country__code__in=AUSTRALIA).distinct().count()

    indonesia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=INDONESIA) | Q(choice_bases__base__country__code__in=INDONESIA) ).distinct().count()

    indonesia_t = Position.objects.filter(  operation__opbase__base__country__code__in=INDONESIA).distinct().count()

    russia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=RUSSIA) | Q(choice_bases__base__country__code__in=RUSSIA) ).distinct().count()

    russia_t = Position.objects.filter(  operation__opbase__base__country__code__in=RUSSIA).distinct().count()

    e_europe_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=E_EUROPE) | Q(choice_bases__base__country__code__in=E_EUROPE) ).distinct().count()

    e_europe_t = Position.objects.filter(  operation__opbase__base__country__code__in=E_EUROPE).distinct().count()

    scandanavia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=SCANDANAVIA) | Q(choice_bases__base__country__code__in=SCANDANAVIA) ).distinct().count()

    scandanavia_t = Position.objects.filter(  operation__opbase__base__country__code__in=SCANDANAVIA).distinct().count()

    canada_h = Status.objects.filter(  Q(assign_bases__base__country__code='CA') | Q(choice_bases__base__country__code='CA') ).distinct().count()

    canada_t = Position.objects.filter(  operation__opbase__base__country__code='CA').distinct().count()

    americas_h = Status.objects.filter(  Q(assign_bases__base__country__continent='SA') | Q(choice_bases__base__country__continent='SA') )
    americas_t = Position.objects.filter(  operation__opbase__base__country__continent='SA').distinct().count()

    carribean_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=CARRIBEAN) | Q(choice_bases__base__country__code__in=CARRIBEAN) ).distinct().count()

    carribean_t = Position.objects.filter(  operation__opbase__base__country__code__in=CARRIBEAN).distinct().count()

    china_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=CHINA) | Q(choice_bases__base__country__code__in=CHINA) ).distinct().count()

    china_t = Position.objects.filter(  operation__opbase__base__country__code__in=CHINA).distinct().count()

    europe_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=EUROPE) | Q(choice_bases__base__country__code__in=EUROPE) ).distinct().count()

    europe_t = Position.objects.filter(  operation__opbase__base__country__code__in=EUROPE).distinct().count()

    middle_east_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=M_EAST) | Q(choice_bases__base__country__code__in=M_EAST) ).distinct().count()

    middle_east_t = Position.objects.filter(  operation__opbase__base__country__code__in=M_EAST).distinct().count()

    return locals()

def overlay(request, z, x, y, o):
    import os
    
    from gtileoverlay.overlays import GTileOverlay
    from django.conf import settings
    
    ICONS_DIR = os.path.join(settings.PROJECT_PATH, 'media', 'icons')

    just_routes = Airport.route.all()
    all_bases = Airport.base.all()

    all_hiring = Airport.hiring.all()
    not_hiring = Airport.not_hiring.all()

    just_hiring = Airport.objects.filter(Q(opbase__choice__in=Status.objects.exclude(advertising=True)) | Q(opbase__assign__in=Status.objects.exclude(advertising=True)))
    #advertising = Airport.objects.filter(Q(opbase__choice__in=Status.objects.filter(advertising=True)) | Q(opbase__assign__in=Status.objects.filter(advertising=True)))

    ##########

    if int(z) < 6:
        size = "/small"
    else:
        size = "/big"

    ov = GTileOverlay(z,x,y, queryset=just_routes, field="location")
    ov.icon(ICONS_DIR + size + '/route.png')                                                                                # light blue icons for route bases

    ov = GTileOverlay(z,x,y, queryset=all_bases, image=ov.output(shuffle=False), field="location")
    ov.icon(ICONS_DIR + size + '/base.png')                                                                         # green icons for no status bases

    ov = GTileOverlay(z,x,y, queryset=all_hiring, image=ov.output(shuffle=False), field="location")                # red for hiring bases
    ov.icon(ICONS_DIR + size + '/hiring.png')

    #ov = GTileOverlay(z,x,y, queryset=advertising, image=ov.output(shuffle=False), field="location")               # red-gold for advertising bases
    #ov.icon(ICONS_DIR + size + '/advertising.png')

    #############################################################

    response = HttpResponse(mimetype="image/png")
    ov.output(shuffle=False).save(response, "PNG")
    return response

@render_to('click.html')
def click(request, lat, lng, z):
    from django.contrib.gis.geos import Point

    point = Point(float(lng), float(lat))   #the point where the user clicked

    airport = Airport.relevant.distance(point).order_by('distance')[0]

    bases = Operation.objects.filter(opbase__base=airport).select_related()
    routes = Operation.objects.filter(opbase__route__bases=airport).select_related()

    return locals()














