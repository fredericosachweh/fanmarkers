from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.db.models import Q

from airport.models import Airport
#from route.models import Route
from models import *

@render_to('view_jobmap.html')
def jobmap(request):
	from django.db.models import Q
	
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

def overlay(request, z, x, y, o):
	from overlay.overlays import GoogleOverlay
	from settings import ICONS_DIR
	
	just_routes = Airport.route.all()
	all_bases = Airport.base.all()
	
	#layoff = all_bases.filter(layoff__in=Status.objects.all())
	
	all_hiring = Airport.hiring.all()
	not_hiring = Airport.not_hiring.all()
	
	just_hiring = Airport.objects.filter(Q(opbase__choice__in=Status.objects.exclude(advertising=True)) | Q(opbase__assign__in=Status.objects.exclude(advertising=True)))
	advertising = Airport.objects.filter(Q(opbase__choice__in=Status.objects.filter(advertising=True)) | Q(opbase__assign__in=Status.objects.filter(advertising=True)))
	
	##########
	
	if int(z) < 6:
		size = "/small"
	else:
		size = "/big"
	
	ov = GoogleOverlay(z,x,y, queryset=just_routes, field="location")
	ov.icon(ICONS_DIR + size + '/route.png')										# light blue icons for route bases
	
	ov = GoogleOverlay(z,x,y, queryset=all_bases, image=ov.output(shuffle=False), field="location")
	ov.icon(ICONS_DIR + size + '/base.png')										# green icons for no status bases
	
	ov = GoogleOverlay(z,x,y, queryset=all_hiring, image=ov.output(shuffle=False), field="location")		# red for hiring bases
	ov.icon(ICONS_DIR + size + '/hiring.png')
	
	ov = GoogleOverlay(z,x,y, queryset=advertising, image=ov.output(shuffle=False), field="location")		# red-gold for advertising bases
	ov.icon(ICONS_DIR + size + '/advertising.png')
	
	#############################################################

	response = HttpResponse(mimetype="image/png")
	ov.output().save(response, "PNG")
	return response

@render_to('click.html')	
def click(request, lat, lng, z):
	from django.contrib.gis.geos import Point
	
	point = Point(float(lng), float(lat))	#the point where the user clicked
	
	airport = Airport.relevant.distance(point).order_by('distance')[0]
	
	bases = Position.objects.filter(operation__opbase__in=OpBase.objects.filter(base=airport)).select_related()
	routes = Position.objects.filter(operation__opbase__in=OpBase.objects.filter(route__in=Route.objects.filter(bases=airport))).select_related()
	
	return locals()
	
	
def kml(request, position=None, company=None, airport=None):
	from django.template.loader import get_template
	from django.http import HttpResponse
	from django.template import Context
	
	if position:
		position = get_object_or_404(Position, pk=position)
		routes = Route.objects.filter(opbase__operation__positions=position)
		bases = Airport.objects.filter(opbase__operation__positions=position).distinct()
		
		routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__positions=position).distinct()
		
		title = str(position.company) + " - " + str(position)
	
	if company:
		company = get_object_or_404(Company, pk=company)
		routes = Route.objects.filter(opbase__operation__company=company)
		bases = Airport.objects.filter(opbase__operation__company=company).distinct()
		
		routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__company=company).distinct()
		
		title = str(company)
		
	if airport:
		bases = get_object_or_404(Airport, pk=airport)
		
				
		title = str(airport)  + " - " + str(bases.name)
		
		bases = [bases]
		
	kml = get_template('base.kml').render(Context(locals() ))

	return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
