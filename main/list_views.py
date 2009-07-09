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

	cat_classes = CAT_CLASSES
	engines = ENGINE_TYPE
	
	aircrafts = Aircraft.objects.all()
	
	if request.GET:

		if request.GET['cat'] != "0":
			aircrafts = aircrafts.filter(cat_class=request.GET['cat'])
		
		if request.GET['engine'] != "0":
			aircrafts = aircrafts.filter(engine_type=request.GET['engine'])
	 

	return locals()
