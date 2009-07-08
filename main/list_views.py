# coding: UTF-8

from main.models import *

from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

########################################################


@render_to('list_position.html')
def position(request, type):

	positions = Position.objects.all()
	
	return locals()
	
@render_to('list_company.html')
def company(request, type):

	companies = Company.objects.all()
	
	return locals()
	
@render_to('list_aircraft.html')
def aircraft(request, type):
	
	aircrafts = Aircraft.objects.all()

	return locals()
