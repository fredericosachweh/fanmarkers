# coding: UTF-8

from jobmap.settings import PROJECT_PATH
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.models import *

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

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
	ops_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))	#ops where this airport is part of a route
	
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

@render_to('edit_operation.html')		
def edit_operation(request, pk):
	from forms import OpBaseForm, OperationForm
	from django.forms.models import inlineformset_factory

	op = Operation.objects.get(pk=pk)

	OpBaseFormSet = inlineformset_factory(Operation, OpBase, form=OpBaseForm, extra=5, )

	if request.method == "POST":
		form    = OperationForm(request.POST, instance=op)
		formset = OpBaseFormSet(request.POST, instance=op)

		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
	
			return HttpResponseRedirect( op.get_absolute_url() )
	else:
		form    = OperationForm(instance=op)
		formset = OpBaseFormSet(instance=op)


	return {'operation': op, 'opform': form, 'formset': formset}

###############################################################################

###############################################################################	

@render_to('edit_status.html')		
def edit_status(request, pk):
	from forms import HiringStatusForm

	pos = Position.objects.get(pk=pk)
	op = Operation.objects.get(positions=pos)
	opbases = op.opbase_set.all()
	bases = Base.objects.filter(opbase__in=opbases)
	
	form = HiringStatusForm(bases_queryset=bases)
	
	return {"form": form, "position": pos}
	
###############################################################################	
	
@render_to('edit_mins.html')	
def edit_mins(request, pk, min_type):
	from forms import CatClassMinsForm, MinsForm
	
	position = Position.objects.get(pk=pk)
	
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

###############################################################################	

@render_to('new_position.html')	
def new_position(request, pk):
	from forms import PositionForm

	company = Company.objects.get(pk=pk)

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

@render_to('new_fleet.html')	
def new_fleet(request, pk):
	from forms import FleetForm

	company = Company.objects.get(pk=pk)

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

@render_to('new_route.html')
def new_route(request, pk):
	from forms import RouteBaseForm, RouteForm
	from django.forms.models import inlineformset_factory
	
	opbase = get_object_or_404(OpBase, pk=pk)
	route = Route(opbase=opbase)
	
	RouteBaseFormset = inlineformset_factory(Route, RouteBase, form=RouteBaseForm, extra=5, )
	
	if request.method == "POST":
		formset = RouteBaseFormset(request.POST)
		routeform = RouteForm(request.POST, instance=route)

		if routeform.is_valid() and formset.is_valid():
			routeform.save()
			return HttpResponseRedirect( "/edit/operation/" + opbase.operation.pk )
	
	else:
		formset = RouteBaseFormset()
		routeform = RouteForm(instance=route)
		
	
	return {"opbase": opbase, "routeform": routeform, "formset": formset}
	
###############################################################################	

@render_to('new_operation.html')	
def new_operation(request, pk):
	from forms import OperationForm, OpBaseForm
	from django.forms.models import inlineformset_factory
	
	company = Company.objects.get(pk=pk)
	
	OpBaseFormset = inlineformset_factory(Operation, OpBase, form=OpBaseForm, extra=5, )
	
	if request.method == "POST":
		blank_op = Operation(company=company)
		form = OperationForm(request.POST, instance=blank_op)
		
		formset = OpBaseFormset(request.POST, instance=blank_op)	#dummy operation instance to make sure the formset validates
		
		if form.is_valid() and formset.is_valid():
			op = form.save()
			formset = OpBaseFormset(request.POST, instance=op)
			formset.save()
			
			return HttpResponseRedirect( "/edit" + company.get_absolute_url() )
	else:
		form = OperationForm(instance=Operation(company=company))
		formset = OpBaseFormset()
		
	return {'company': company, 'form': form, "formset": formset}


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
from main.overlays import overlay_view
	

	
	
	
	
	
