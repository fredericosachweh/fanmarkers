from models import *
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404

from main.models import Operation, Company, OpBase, Route

@render_to('view_airport.html')
def airport(request, pk):

	airport = get_object_or_404(Airport, pk=pk)
	
	company_base = 	Company.objects.filter(operation__opbase__base=airport)								#ops where this airport is a base
	ops_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(route__in=Route.objects.filter(bases=airport)))	#ops where this airport is part of a route
	
	return locals()
