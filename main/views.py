# coding: UTF-8

from jobmap.settings import PROJECT_PATH
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import *
from annoying.decorators import render_to
from annoying.functions import get_object_or_None


@render_to('view/jobmap.html')
def jobmap(request):
	from django.contrib.sites.models import Site

	domain = Site.objects.get_current().domain
	
	#usa_jobs = OpBase.objects.filter(

	return {"domain": domain}

###############################################################################	
	
@render_to('view/position.html')		
def position(request, pk):

	position = get_object_or_None(Position, pk=pk)
	
	if not position:
		fail = True
	else:
		fail = False

	#try:
	#	position = Position.objects.select_related().get(pk=pk)
	#except:
	#	fail=True

	return {'p': position, "not_found": fail}

###############################################################################	
	
@render_to('view/company.html')		
def company(request, pk):

	company=""
	fail=""

	try:
		company = Company.objects.select_related().get(pk=pk)
	except:
		fail=True
		
	return {'c': company, "not_found": fail}

###############################################################################	
	
@render_to('view/airport.html')
def airport(request, pk):

	airport = get_object_or_None(Base, pk=pk)
	
	fail = not airport	#if airport = None, then fail = true.
	
	ops_base = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))					#ops where this airport is a base
	ops_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))	#ops where this airport is part of a route
	
	return {'a': airport, "ops_base": ops_base, "ops_fly": ops_fly, "not_found": fail}
	
###############################################################################	
	
@render_to('view/aircraft.html')
def aircraft(request, pk):

	aircraft = get_object_or_None(Aircraft, pk=pk)
	
	if not aircraft:				#if aircraft = None, then return 404.
		return {"not_found": True}
		
	operations = Operation.objects.filter(fleet__in=Fleet.objects.filter(aircraft=aircraft))
	
	return {'aircraft': aircraft, "operations": operations}
	

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

@render_to('edit/edit_company.html')	
def edit_company(request, pk):
	from forms import CompanyForm
	
	company = Company.objects.get(pk=pk)
	
	if request.method == "POST":
		form = CompanyForm(request.POST, instance=company)
		
		if not form.errors:
			form.save()
	else:
		form = CompanyForm(instance=company)
	
	return {'company': company, 'form': form}
	
###############################################################################		

@render_to('edit/edit_operation.html')		
def edit_operation(request, pk):
	from forms import OpBaseForm, OperationForm
	from django.forms.models import modelformset_factory

	op = Operation.objects.get(pk=pk)
	
	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm, exclude=['routes', 'operation', ], extra=3, can_delete=True, )
	
	if request.method == "POST":
		opform  = OperationForm(request.POST, instance=op)
		formset = OpBaseFormSet(request.POST, queryset=op.opbase_set.all())
		
		if formset.is_valid() and opform.is_valid():
			opform.save()
			
			instances = formset.save(commit=False)
			
			for instance in instances:
				instance.operation = op
				instance.save()
			
			return HttpResponseRedirect('/edit/company/' + str(op.company.pk)) # Redirect after POST
	else:
		formset = OpBaseFormSet(queryset=op.opbase_set.all())
		opform  = OperationForm(instance=op)

	return {'operation': op, 'opform': opform, 'formset': formset}

###############################################################################	

@render_to('edit/edit_position.html')		
def edit_position(request, pk):
	from forms import PositionForm, HiringStatusForm

	p = Position.objects.get(pk=pk)
	
	try:
		hs= p.hiringstatus_set.all()[0]
	except:
		hs=HiringStatus(position=p)
		
	if request.method == "POST":
		pos_form = PositionForm(request.POST, instance=p)
		
		if not pos_form.errors:
			pos_form.save()
			return HttpResponseRedirect('/edit/company/' + str(op.company.pk)) # Redirect after POST
	else:
		pos_form = PositionForm(instance=p)
		
		
	return {'position': p, 'pos_form': pos_form}

###############################################################################	

@render_to('edit/edit_route.html')		
def edit_route(request, pk):
	from forms import PositionForm

	r = Route.objects.get(pk=pk)
	form = RouteForm(instance=p)
	
	new_form = RouteForm()
	
	return {'route': r, 'form': form, 'new_form': new_form}
	
###############################################################################	

@render_to('edit/edit_fleet.html')	
def edit_fleet(request, pk):
	from forms import FleetForm

	fleet = Fleet.objects.get(pk=pk)
	
	
	if request.method == "POST":
		form = FleetForm(request.POST, instance=fleet)
		
		if not form.errors:
			form.save()
			return HttpResponseRedirect('/edit/company/' + str(fleet.company.pk)) # Redirect after POST
	else:
		form = FleetForm(instance=fleet)
	
	return {'fleet': fleet, 'form': form}
	
###############################################################################	

@render_to('edit/edit_status.html')		
def edit_status(request, pk):
	from forms import HiringStatusForm

	pos = Position.objects.get(pk=pk)
	op = Operation.objects.get(positions=pos)
	opbases = op.opbase_set.all()
	bases = Base.objects.filter(opbase__in=opbases)
	
	form = HiringStatusForm(bases_queryset=bases)
	
	return {"form": form, "position": pos}
	
###############################################################################	
	
@render_to('edit/edit_mins.html')	
def edit_mins(request, pk, min_type):
	from forms import CatClassMinsForm, MinsForm
	
	position = Position.objects.get(pk=pk)
	
	#############################
	
	if min_type == "Hard":
		mins_object = position.hard_mins
		if not mins_object:
			mins_object = Mins()
			mins_object.save()
			
			position.hard_mins = mins_object
			position.save()
	else:
		mins_object = position.pref_mins
		if not mins_object:				#if mins object hasnt been created yet, then create it!
			mins_object = Mins()
			mins_object.save()
			
			position.pref_mins = mins_object
			position.save()
	
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
			return HttpResponseRedirect('/edit/position/' + str(position.pk)) # Redirect after POST
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

@render_to('new/new_company.html')	
def new_company(request):
	from forms import CompanyForm
	
	if request.method == "POST":
		form = CompanyForm(request.POST)
		
		if not form.errors:
			form.save()
			return HttpResponseRedirect('/edit/company/' + str(form.instance.id)) # Redirect after POST
	
	form = CompanyForm()
		
	return {'company': company, 'form': form}
	
###############################################################################	

@render_to('new/new_operation.html')	
def new_operation(request, pk):
	from forms import OperationForm
	
	company = Company.objects.get(pk=pk)
	
	if request.method == "POST":
		op = Operation(company=company)
		form = OperationForm(request.POST, instance=op)
		
		if not form.errors:
			form.save()
			return HttpResponseRedirect('/edit/company/' + str(pk)) # Redirect after POST
	
	form = OperationForm(instance=Operation(company=company))
		
	return {'company': company, 'form': form}
	
###############################################################################	

@render_to('new/new_position.html')	
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
			return HttpResponseRedirect('/edit/company/' + str(pk)) # Redirect after POST
			
	form = PositionForm()
	
	return {'company': company, 'form': form}
	
###############################################################################	

@render_to('new/new_fleet.html')	
def new_fleet(request, pk):
	from forms import FleetForm

	company = Company.objects.get(pk=pk)

	if request.method == "POST":
		fleet = Fleet(company=company)
		form = FleetForm(request.POST, instance=fleet)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/edit/company/' + str(pk)) # Redirect after POST
	
	form = FleetForm()
		
	return {'company': company, 'form': form}
	
###############################################################################	

@render_to('new/new_route.html')
def new_route(request, pk):
	from forms import RouteForm

	ob = OpBase.objects.get(pk=pk)
	
	if request.method == "POST":
		route = Route(opbase=ob)
		form = RouteForm(request.POST, instance=route)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/edit/operation/' + str(pk)) # Redirect after POST
	
	form = RouteForm()
	
	return {'opbase': ob, 'form': form}


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def overlay(request, z, x, y, o):
	from main.overlays import *
	from jobmap.settings import ICONS_DIR
	
	if o[0] == "B":
		ov = BaseOverlay(z, x, y, o)
		ov.hard_limit = 10000
		
		if z<4:		#zoomed out
			ov.icon(ICONS_DIR + '/small/dblue.png')
	
		elif z>=4:		#zoomd in close
			ov.icon(ICONS_DIR + '/big/dblue.png')
			
	#############################################################	
		
	elif o[0]=="D":
		ov = DestinationOverlay(z, x, y, o)
		ov.hard_limit = 10000
	
		if z<4:		#zoomed out
			ov.icon(ICONS_DIR + '/tiny/red.png')
	
		elif z>=4:		#zoomd in close
			ov.icon(ICONS_DIR + '/small/red.png')	
	
	
	response = HttpResponse(mimetype="image/png")
	ov.output().save(response, "PNG")
	return response
	

	
	
	
	
	
