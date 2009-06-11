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
	
	if not airport:
		fail = True
	else:
		fail = False
		
	#ops_base = []
	#ops_fly = []
	
	op_base = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))
	op_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))
	
	
	#for op in op_base:
	#	ops_base.append(op)
		
	#for op in op_fly:
	#	ops_fly.append(op)
	
	return {'a': airport, "ops_base": op_base, "ops_fly": op_fly}
	

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
	from forms import OpBaseForm
	from django.forms.models import modelformset_factory

	op = Operation.objects.get(pk=pk)
	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm, exclude=['routes'], extra=0)
	
	if request.method == "POST":
		formset = OpBaseFormSet(request.POST)
	
	
	formset = OpBaseFormSet(queryset=op.opbase_set.all())
	
	new_form = OpBaseForm()

	return {'operation': op, 'formset': formset, 'new_form': new_form}

###############################################################################	

@render_to('edit/edit_position.html')		
def edit_position(request, pk):
	from forms import PositionForm, MinsForm

	p = Position.objects.get(pk=pk)
	
	if request.method == "POST":
		form = PositionForm(request.POST, instance=p)
		
		if not form.errors:
			form.save()
	else:
		try:
			base_mins = p.base_mins
			
		except:
			base_mins = Mins()
			
		try:
			pref_mins = p.pref_mins
		except:
			pref_mins = Mins()
	
		pos_form = PositionForm(instance=p)
		hard_form= MinsForm(instance=base_mins)
		pref_form= MinsForm(instance=pref_mins)
		
	return {'position': p, 'pos_form': pos_form, "hard_form": hard_form, "pref_form": pref_form}

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
	from forms import PositionForm

	r = Route.objects.get(pk=pk)
	form = RouteForm(instance=p)
	
	new_form = RouteForm()
	
	return {'route': r, 'form': form, 'new_form': new_form}
	
###############################################################################	

@render_to('edit/edit_hiring_status.html')		
def edit_hiring_status(request, pk):
	from forms import HiringStatusForm

	company = Company.objects.get(pk=pk)
	
	form = HiringStatusForm()
	
	return {"form": form}

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
	

	
	
	
	
	
