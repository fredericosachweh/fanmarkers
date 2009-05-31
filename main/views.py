# coding: UTF-8

from jobmap.settings import PROJECT_PATH
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import *

def jobmap(request):
	from settings import GOOGLE_MAPS_KEY
	from django.contrib.sites.models import Site

	Site.objects.clear_cache()
	domain = Site.objects.get_current().domain
	c = RequestContext(request, {'maps_key': GOOGLE_MAPS_KEY, 'domain': domain})
	return render_to_response('map.html', c)
	
def company(request, company_id):

	company=""
	fail=""

	try:
		company = Company.objects.select_related().get(pk=company_id)
	except:
		fail=True

	c = RequestContext(request, {'c': company, "not_found": fail} )
	return render_to_response('company.html', c )
	
def company_master_list(request):

	companies = Company.objects.all()[:50]				# get the first 50 companies
	
	c = RequestContext(request, {'companies': companies} )
	return render_to_response('company_master_list.html', c )
	
def airport(request, airport_id):

	airport=""
	fail=""

	try:
		airport = Base.objects.select_related().get(pk=airport_id)
	except:
		c = RequestContext(request, {"not_found": True} )
		return render_to_response('airport.html', c )
		
	###################
	ops_base = []
	ops_fly = []
	
	op_based = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))
	op_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))
	
	
	for op in op_based:
		ops_base.append(op)
		
	for op in op_fly:
		ops_fly.append(op)
	
	
	c = RequestContext(request, {'a': airport, "ops_base": ops_base, "ops_fly": ops_fly, "not_found": fail} )
	return render_to_response('airport.html', c )
	
def edit_company(request, company_id):
	from forms import CompanyForm
	
	company = Company.objects.get(pk=company_id)
	company_form = CompanyForm(instance=company)
	
	operations = []
	
	for op in company.operation_set.all():
		operations.append(op)
	
	c = RequestContext(request, {'c': company, 'company_form': company_form, 'operations': operations} )
	return render_to_response('company_edit.html', c )
	
def edit_operation(request, op_id):
	from forms import OpBaseForm
	from django.forms.models import modelformset_factory

	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm)
	op = Operation.objects.get(pk=op_id)
	formset = OpBaseFormSet(queryset=op.opbase_set.all())

	c = RequestContext(request, {'operation': op, 'formset': formset} )
	return render_to_response('operation_edit.html', c )
	
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
	

	
	
	
	
	
