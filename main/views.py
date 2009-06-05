# coding: UTF-8

from jobmap.settings import PROJECT_PATH
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import *

def jobmap(request):
	from settings import GOOGLE_MAPS_KEY
	from django.contrib.sites.models import Site

	domain = Site.objects.get_current().domain
	c = RequestContext(request,)
	return render_to_response('view/jobmap.html', c)
	
def position(request, pk):

	company=""
	fail=""

	try:
		position = Position.objects.select_related().get(pk=pk)
	except:
		fail=True

	c = RequestContext(request, {'p': position, "not_found": fail} )
	return render_to_response('view/position.html', c )
	
def company(request, pk):

	company=""
	fail=""

	try:
		company = Company.objects.select_related().get(pk=pk)
	except:
		fail=True

	c = RequestContext(request, {'c': company, "not_found": fail} )
	return render_to_response('view/company.html', c )
	
def airport(request, pk):

	airport=""
	fail=""

	try:
		airport = Base.objects.select_related().get(pk=airport_id)
	except:
		c = RequestContext(request, {"not_found": True} )
		return render_to_response('view/airport.html', c )
		
	ops_base = []
	ops_fly = []
	
	op_based = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))
	op_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))
	
	
	for op in op_based:
		ops_base.append(op)
		
	for op in op_fly:
		ops_fly.append(op)
	
	
	c = RequestContext(request, {'a': airport, "ops_base": ops_base, "ops_fly": ops_fly, "not_found": fail} )
	return render_to_response('view/airport.html', c )
	

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
	
def edit_company(request, pk):
	from forms import CompanyForm
	
	company = Company.objects.get(pk=pk)
	company_form = CompanyForm(instance=company)
	
	c = RequestContext(request, {'company': company, 'form': company_form} )
	return render_to_response('edit/edit_company.html', c )
	
def edit_operation(request, pk):
	from forms import OpBaseForm
	from django.forms.models import modelformset_factory

	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm, exclude=['routes'], extra=0)
	op = Operation.objects.get(pk=pk)
	formset = OpBaseFormSet(queryset=op.opbase_set.all())
	
	new_form = OpBaseForm()

	c = RequestContext(request, {'operation': op, 'formset': formset, 'new_form': new_form} )
	return render_to_response('edit/edit_operation.html', c )
	
def edit_position(request, pk):
	from forms import PositionForm

	p = Position.objects.get(pk=pk)
	form = PositionForm(instance=p)
	
	new_form = PositionForm()
	
	c = RequestContext(request, {'position': p, 'form': form, 'new_form': new_form} )
	return render_to_response('edit/edit_position.html', c )
	
def edit_route(request, pk):
	from forms import PositionForm

	r = Route.objects.get(pk=pk)
	form = RouteForm(instance=p)
	
	new_form = RouteForm()
	
	c = RequestContext(request, {'route': r, 'form': form, 'new_form': new_form} )
	return render_to_response('edit/edit_route.html', c )

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
	
def new_company(request):
	from forms import CompanyForm
	
	form = CompanyForm()
		
	c = RequestContext(request, {'c': company, 'form': form} )
	return render_to_response('new/new_company.html', c )
	
def new_operation(request, pk):
	from forms import OpBaseForm
	from django.forms.models import modelformset_factory

	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm, exclude=['routes'], extra=0)
	op = Operation.objects.get(pk=pk)
	formset = OpBaseFormSet(queryset=op.opbase_set.all())
	
	new_form = OpBaseForm()

	c = RequestContext(request, {'operation': op, 'formset': formset, 'new_form': new_form} )
	return render_to_response('new/new_operation.html', c )
	
def new_position(request, pk):
	from forms import PositionForm

	p = Position.objects.get(pk=pk)
	form = PositionForm(instance=p)
	
	new_form = PositionForm()
	
	c = RequestContext(request, {'position': p, 'form': form, 'new_form': new_form} )
	return render_to_response('new/new_position.html', c )
	
def new_route(request, pk):
	from forms import PositionForm

	p = Position.objects.get(pk=pk)
	form = PositionForm(instance=p)
	
	new_form = PositionForm()
	
	c = RequestContext(request, {'position': p, 'form': form, 'new_form': new_form} )
	return render_to_response('new/new_route.html', c )


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
	

	
	
	
	
	
