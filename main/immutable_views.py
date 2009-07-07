from django.contrib.auth.decorators import login_required
from main.models import *

from annoying.decorators import render_to
from django.shortcuts import get_object_or_404

@render_to('view_jobmap.html')
def jobmap(request):
	from django.db.models import Q
	
	usa_bases = Airport.objects.filter(country__exact="US")
	alaska_bases = usa_bases.filter(region__name__exact="AK")
	russia_bases = Airport.objects.filter(country__exact="RU")
	india_bases = Airport.objects.filter(country__exact="IN")
	canada_bases = Airport.objects.filter(country__exact="CA")
	
	usa_h = Status.objects.filter(   Q(assign_bases__in=usa_bases) | Q(choice_bases__in=usa_bases)    ).distinct().count()
	usa_t = Position.objects.filter( operation__bases__in=usa_bases ).distinct().count()

	canada_h = Status.objects.filter(   Q(assign_bases__in=canada_bases) | Q(choice_bases__in=canada_bases)    ).distinct().count()
	canada_t = Position.objects.filter( operation__bases__in=canada_bases ).distinct().count()
	
	india_h = Status.objects.filter(   Q(assign_bases__in=india_bases) | Q(choice_bases__in=india_bases)    ).distinct().count()
	india_t = Position.objects.filter( operation__bases__in=india_bases ).distinct().count()

	russia_h = Status.objects.filter(   Q(assign_bases__in=russia_bases) | Q(choice_bases__in=russia_bases)    ).distinct().count()
	russia_t = Position.objects.filter( operation__bases__in=russia_bases ).distinct().count()
	
	alaska_h = Status.objects.filter(   Q(assign_bases__in=alaska_bases) | Q(choice_bases__in=alaska_bases)    ).distinct().count()
	alaska_t = Position.objects.filter( operation__bases__in=alaska_bases ).distinct().count()

	return locals()

###############################################################################	
	
@render_to('view_airport.html')
def airport(request, pk):

	airport = get_object_or_404(Airport, pk=pk)
	
	ops_base = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))					#ops where this airport is a base
	ops_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(route__in=Route.objects.filter(bases=airport)))	#ops where this airport is part of a route
	
	return {'airport': airport, "ops_base": ops_base, "ops_fly": ops_fly}
	
###############################################################################
	
@render_to('view_aircraft.html')
def aircraft(request, pk):

	aircraft = get_object_or_404(Aircraft, pk=pk)
	operations = Operation.objects.filter(fleet__in=Fleet.objects.filter(aircraft=aircraft))
	
	return {'aircraft': aircraft, "operations": operations}
