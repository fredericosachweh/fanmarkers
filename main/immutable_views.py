from django.contrib.auth.decorators import login_required
from main.models import *

from annoying.decorators import render_to
from django.shortcuts import get_object_or_404

@render_to('view_jobmap.html')
def jobmap(request):
	from django.db.models import Q
	
	#usa_bases = Base.objects.filter(country__exact="United States")
	
	#all_hiring = Position.objects.exclude(status__choice_bases__isnull=True, status__assign_bases__isnull=True).values('pk')
	#just_hiring = all_hiring.exclude(status__advertising=True)
	#advertising = all_hiring.filter(status__advertising=True)
	#layoff = Status.objects.filter(layoff_bases__isnull=False).values('pk')
	
	usa_h = "ff" #Status.objects.filter(   Q(assign_bases__in=usa_bases) | Q(choice_bases__in=usa_bases)    ).count()

	return {"usa_h": usa_h}

###############################################################################	
	
@render_to('view_airport.html')
def airport(request, pk):

	airport = get_object_or_404(Base, pk=pk)
	
	ops_base = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))					#ops where this airport is a base
	ops_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(route__in=Route.objects.filter(bases=airport)))	#ops where this airport is part of a route
	
	return {'airport': airport, "ops_base": ops_base, "ops_fly": ops_fly}
	
###############################################################################
	
@render_to('view_aircraft.html')
def aircraft(request, pk):

	aircraft = get_object_or_404(Aircraft, pk=pk)
	operations = Operation.objects.filter(fleet__in=Fleet.objects.filter(aircraft=aircraft))
	
	return {'aircraft': aircraft, "operations": operations}
