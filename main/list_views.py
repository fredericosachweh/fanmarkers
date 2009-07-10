# coding: UTF-8

from main.models import *
from main.constants import *

from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

########################################################


@render_to('list_position.html')
def position(request):

	positions = Position.objects.all()
	
	return locals()
	
@render_to('list_company.html')
def company(request):

	companies = Company.objects.all()
	
	return locals()
	
@render_to('list_aircraft.html')
def aircraft(request):
	from main.forms import AircraftSearch

	cat_classes = CAT_CLASSES
	engines = ENGINE_TYPE
	
	aircrafts = Aircraft.objects.all()
	
	if request.GET:
	
		searchform = AircraftSearch(request.GET)
		
		if searchform.is_valid():

			if searchform.cleaned_data["cat_class"] != "0":
				aircrafts = aircrafts.filter(cat_class=searchform.cleaned_data["cat_class"])
		
			if searchform.cleaned_data["engine_type"] != "0":
				aircrafts = aircrafts.filter(engine_type=searchform.cleaned_data["engine_type"])
		 
		 	if searchform.cleaned_data["search"]:
				s = searchform.cleaned_data["search"]
				aircrafts = aircrafts.filter( Q(manufacturer__icontains=s) | Q(type__icontains=s) | Q(model__icontains=s) | Q(extra__icontains=s) )
				
	else:
		searchform = AircraftSearch()

	return locals()
