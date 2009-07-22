from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.db.models import Q

from airport.models import Airport
from models import *

@render_to('view_jobmap.html')
def jobmap(request):
    from django.db.models import Q

    INDIA =       ['IN','LK']
    AUSTRALIA =   ['AU','NZ','NC','VU','FJ','AS','TO','TV','TK','WF','CK','NU','PF']
    M_EAST =      ['AE','AM','AF','BH','IR','IQ','IL','JO','KW','LB','YE','SY','OM','QA','PK']
    E_EUROPE =    ['TR','GR','HU','MD','PL','BY','SK','CZ','RO','HR','BA','AL','MK','ME','CY','SI','LT','LV','EE']
    INDONESIA =   ['ID','PG','SG','MY','PH']
    SCANDANAVIA = ['IS','NO','SE','FI']
    CHINA =       ['KP','KR','MN','HK','MO']
    EUROPE =      ['FR','UK','IT','DK','DE','IE', 'PT','ES','LU','AD','VA','SM','IM','','']
    RUSSIA =      ['RU','','',]
    CARRIBEAN =   ['AG','AI','AN','AW','BB','BL','BM','BS','CU','DM','DO','GD','GP','HT','JM','KN','KY','LC','MF','MQ','MS','PM','PR','TC','TT','VC','VG','VI']
    AMERICAS =    ['MX','SV','PA','NI','HN','BZ','GT','CR']


    africa_h = Status.objects.filter(  Q(assign_bases__base__country__continent='AF') | Q(choice_bases__base__country__continent='AF') ).count()
    africa_t = Position.objects.filter(  operation__opbase__base__country__continent='AF' ).count()

    usa_h = Status.objects.filter(  Q(assign_bases__base__country__code='US') | Q(choice_bases__base__country__code='US') ).count()
    usa_t = Position.objects.filter(  operation__opbase__base__country__code='US').count()

    alaska_h = Status.objects.filter(  Q(assign_bases__base__region__code='US-AK') | Q(choice_bases__base__region__code='US-AK') )
    alaska_t = Position.objects.filter(  operation__opbase__base__region__code='US-AK').count()

    india_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=INDIA) | Q(choice_bases__base__country__code__in=INDIA) )
    india_t = Position.objects.filter(  operation__opbase__base__country__code__in=INDIA).count()

    australia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=AUSTRALIA) | Q(choice_bases__base__country__code__in=AUSTRALIA) )
    australia_t = Position.objects.filter(  operation__opbase__base__country__code__in=AUSTRALIA).count()

    indonesia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=INDONESIA) | Q(choice_bases__base__country__code__in=INDONESIA) )
    indonesia_t = Position.objects.filter(  operation__opbase__base__country__code__in=INDONESIA).count()

    russia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=RUSSIA) | Q(choice_bases__base__country__code__in=RUSSIA) )
    russia_t = Position.objects.filter(  operation__opbase__base__country__code__in=RUSSIA).count()

    e_europe_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=E_EUROPE) | Q(choice_bases__base__country__code__in=E_EUROPE) )
    e_europe_t = Position.objects.filter(  operation__opbase__base__country__code__in=E_EUROPE).count()

    scandanavia_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=SCANDANAVIA) | Q(choice_bases__base__country__code__in=SCANDANAVIA) );scandanavia_t = Position.objects.filter(  operation__opbase__base__country__code__in=SCANDANAVIA).count()

    canada_h = Status.objects.filter(  Q(assign_bases__base__country__code='CA') | Q(choice_bases__base__country__code='CA') )
    canada_t = Position.objects.filter(  operation__opbase__base__country__code='CA').count()

    americas_h = Status.objects.filter(  Q(assign_bases__base__country__continent='SA') | Q(choice_bases__base__country__continent='SA') )
    americas_t = Position.objects.filter(  operation__opbase__base__country__continent='SA').count()

    carribean_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=CARRIBEAN) | Q(choice_bases__base__country__code__in=CARRIBEAN) )
    carribean_t = Position.objects.filter(  operation__opbase__base__country__code__in=CARRIBEAN).count()

    china_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=CHINA) | Q(choice_bases__base__country__code__in=CHINA) )
    china_t = Position.objects.filter(  operation__opbase__base__country__code__in=CHINA).count()

    europe_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=EUROPE) | Q(choice_bases__base__country__code__in=EUROPE) )
    europe_t = Position.objects.filter(  operation__opbase__base__country__code__in=EUROPE).count()

    middle_east_h = Status.objects.filter(  Q(assign_bases__base__country__code__in=M_EAST) | Q(choice_bases__base__country__code__in=M_EAST) )
    middle_east_t = Position.objects.filter(  operation__opbase__base__country__code__in=M_EAST).count()

    return locals()

def overlay(request, z, x, y, o):
    from overlay.overlays import GoogleOverlay
    from settings import ICONS_DIR

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

    ov = GoogleOverlay(z,x,y, queryset=just_routes, field="location")
    ov.icon(ICONS_DIR + size + '/route.png')                                                                                # light blue icons for route bases

    ov = GoogleOverlay(z,x,y, queryset=all_bases, image=ov.output(shuffle=False), field="location")
    ov.icon(ICONS_DIR + size + '/base.png')                                                                         # green icons for no status bases

    ov = GoogleOverlay(z,x,y, queryset=all_hiring, image=ov.output(shuffle=False), field="location")                # red for hiring bases
    ov.icon(ICONS_DIR + size + '/hiring.png')

    #ov = GoogleOverlay(z,x,y, queryset=advertising, image=ov.output(shuffle=False), field="location")               # red-gold for advertising bases
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

    bases = Position.objects.filter(operation__opbase__base=airport).select_related()
    routes = Position.objects.filter(operation__opbase__route__bases=airport).select_related()

    return locals()


def kml(request, position=None, company=None, airport=None):
    from django.template.loader import get_template
    from django.http import HttpResponse
    from django.template import Context
    from route.models import Route

    if position:
        position = get_object_or_404(Position, pk=position)
        routes = Route.objects.filter(home__operation__positions=position)
        bases = Airport.objects.filter(opbase__operation__positions=position).distinct()
        routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__positions=position).distinct()
        title = str(position.company) + " - " + str(position)

    if company:
        company = get_object_or_404(Company, pk=company)
        routes = Route.objects.filter(home__operation__company=company)
        bases = Airport.objects.filter(opbase__operation__company=company).distinct()
        routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__company=company).distinct()
        title = str(company)

    if airport:
        base = get_object_or_404(Airport, pk=airport)
        title = str(airport)  + " - " + str(base.name)
        bases = [base]          #make it a list so it can be iterated in the template

    kml = get_template('base.kml').render(Context(locals() ))
    return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
