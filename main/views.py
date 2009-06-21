# coding: UTF-8

from jobmap.settings import PROJECT_PATH
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from main.models import *

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

def sortdict(d):
    """ returns a dictionary sorted by keys """
    our_list = d.items()
    our_list.sort()
    k = {}
    for item in our_list:
        k[item[0]] = item[1]
    return k


###############################################################################

@render_to('view_jobmap.html')
def jobmap(request):
	
	usa = OpBase.objects.filter(id=1)

	return {"usa": usa}

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
	

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


###############################################################################		

@login_required()
@render_to('edit_operation.html')		
def edit_operation(request, pk):
	from forms import OpBaseFormset, OperationForm

	op = get_object_or_404(Operation, pk=pk)

	if request.method == "POST":
		form    = OperationForm(request.POST, instance=op)
		formset = OpBaseFormset(request.POST, instance=op)

		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
	
			return HttpResponseRedirect( op.get_absolute_url() )
	else:
		form    = OperationForm(instance=op)
		formset = OpBaseFormset(instance=op)


	return {'operation': op, 'opform': form, 'formset': formset}

###############################################################################

@login_required()
@render_to('edit_status.html')		
def edit_status(request, pk):
	from forms import StatusForm
	import datetime

	position = get_object_or_404(Position, pk=pk)
	operation = Operation.objects.get(positions=position)
	opbases = operation.opbase_set.all()
	bases = Base.objects.filter(opbase__in=opbases)
	
	now = datetime.datetime.now()
	
	status = get_object_or_None(Status, position=position)
	
	if not status:
		status = Status(position=position, date=now)
	
	#assert False
	
	array = {}
	array["unknown"] = array["assign"] = array["choice"] = array["advertising"] = array["layoff"] = []
	
	if request.method == "POST":
		
		form = StatusForm(request.POST, instance=status)
		
	
		for base in bases:
			for item in ("unknown", "assign", "choice", "advertising", "layoff", ):
				if request.POST[str(base)] == item:
					array[item] = array[item] + [base]
		if form.is_valid():
			form = form.save(commit=False)
			form.advertising = array["advertising"]
			form.save()
	
	else:
		form = StatusForm()
	
	return {"form": form, "position": position, "bases": bases}
	
###############################################################################	

@login_required()	
@render_to('edit_mins.html')	
def edit_mins(request, pk, min_type):
	from forms import CatClassMinsForm, MinsForm
	
	position = get_object_or_404(Position, pk=pk)
	
	#############################
	
	if min_type == "Hard":
		mins_object = position.hard_mins
		if not mins_object:
			mins_object = Mins()

	else:
		mins_object = position.pref_mins
		if not mins_object:				#if mins object hasnt been created yet, then create it!
			mins_object = Mins()
	
	#############################
	
	
			
	anyy =		mins_object.any_mins
	airplane =	mins_object.airplane_mins
	se =		mins_object.se_mins
	me =		mins_object.me_mins
	sea =		mins_object.sea_mins
	mes =		mins_object.mes_mins
	heli =		mins_object.heli_mins
	glider =	mins_object.glider_mins
	sim =		mins_object.sim_mins
	
	if request.method == "POST":
		general_mins = MinsForm(request.POST, instance=mins_object, prefix="gen")
		
		any_mins = CatClassMinsForm(request.POST, instance=anyy, prefix="any")
		airplane_mins = CatClassMinsForm(request.POST, instance=airplane, prefix="airplane")
		se_mins = CatClassMinsForm(request.POST, instance=se, prefix="se")
		me_mins = CatClassMinsForm(request.POST, instance=me, prefix="me")
		sea_mins = CatClassMinsForm(request.POST, instance=sea, prefix="sea")
		mes_mins = CatClassMinsForm(request.POST, instance=mes, prefix="mes")
		heli_mins = CatClassMinsForm(request.POST, instance=heli, prefix="heli")
		glider_mins = CatClassMinsForm(request.POST, instance=glider, prefix="glider")
		sim_mins = CatClassMinsForm(request.POST, instance=sim, prefix="sim")
		
		if not general_mins.errors and not any_mins.errors:
			general_mins.save()
			any_mins.save()
			se_mins.save()
			me_mins.save()
			sea_mins.save()
			mes_mins.save()
			heli_mins.save()
			glider_mins.save()
			sim_mins.save()
			
			return HttpResponseRedirect( position.get_absolute_url() )
	else:
		any_mins = CatClassMinsForm(instance=anyy, prefix="any")
		airplane_mins = CatClassMinsForm(instance=airplane, prefix="airplane")
		se_mins = CatClassMinsForm(instance=se, prefix="se")
		me_mins = CatClassMinsForm(instance=me, prefix="me")
		sea_mins = CatClassMinsForm(instance=sea, prefix="sea")
		mes_mins = CatClassMinsForm(instance=mes, prefix="mes")
		heli_mins = CatClassMinsForm(instance=heli, prefix="heli")
		glider_mins = CatClassMinsForm(instance=glider, prefix="glider")
		sim_mins = CatClassMinsForm(instance=sim, prefix="sim")
		
		general_mins = MinsForm(instance=mins_object, prefix="gen")
	
	return locals()
	
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

@login_required()
@render_to('new_position.html')	
def new_position(request, pk):
	from forms import PositionForm

	company = get_object_or_404(Company, pk=pk)

	if request.method == "POST":
		pos = Position(company=company)
		form = PositionForm(request.POST, instance=pos)
	
		if form.is_valid():
			form.save(commit=False)
			form.hard_mins = Mins()
			form.pref_mins = Mins()
			form.save()
			return HttpResponseRedirect( "/edit" + company.get_absolute_url() )
	else:
		form = PositionForm()
	
	return {'company': company, 'form': form}
	
###############################################################################	

@login_required()
@render_to('new_fleet.html')	
def new_fleet(request, pk):
	from forms import FleetForm

	company = get_object_or_404(Company, pk=pk)

	if request.method == "POST":
		fleet = Fleet(company=company)
		form = FleetForm(request.POST, instance=fleet)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( "/edit" + company.get_absolute_url() )
	else:
		form = FleetForm()
		
	return {'company': company, 'form': form}
	
###############################################################################	

@login_required()
@render_to('new-edit_route.html')
def handle_route(request, ttype, pk):
	from forms import RouteBaseFormset, RouteForm

	if ttype=="new":
		opbase = get_object_or_404(OpBase, pk=pk)
		route = Route(opbase=opbase)
	elif ttype=="edit":
		route = get_object_or_404(Route, pk=pk)
		opbase = route.opbase
		
	if request.method == "POST":	
		newPOST = request.POST.copy()
		
		i=1
		for index in range(0, int(request.POST["routebase_set-TOTAL_FORMS"])):
			if request.POST["routebase_set-" + str(index) + "-base"]:
				newPOST["routebase_set-" + str(index) + "-sequence"]=i
				i += 1
			else:
				newPOST["routebase_set-" + str(index) + "-sequence"] = ""
		
		########################################################
		formset = RouteBaseFormset(newPOST)
		routeform = RouteForm(request.POST, instance=route)
		
		if routeform.is_valid() and formset.is_valid():
			route = routeform.save()
			formset = RouteBaseFormset(newPOST, instance=route)
			formset.save()
						
			return HttpResponseRedirect( "/edit/operation/" + str(opbase.operation.pk) )
	
	else:
		if ttype=="new":
			formset = RouteBaseFormset()
			routeform = RouteForm(instance=route)
		elif ttype=="edit":	
			formset = RouteBaseFormset(instance=route)
			routeform = RouteForm(instance=route)
		
	return {"type": ttype, "opbase": opbase, "routeform": routeform, "formset": formset}
	
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
from main.overlays import overlay_view
	

	
	
	
	
	
