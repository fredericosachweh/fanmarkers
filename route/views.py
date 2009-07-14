from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.db.models import Q

from models import *
from forms import *


@login_required()
@render_to('new-edit_route.html')
def handle_route(request, type, pk):

	if type=="new":
		opbase = get_object_or_404(OpBase, pk=pk)
		route = Route(opbase=opbase)
	elif type=="edit":
		route = get_object_or_404(Route, pk=pk)
		opbase = route.opbase
		
	if request.method == "POST":	
		newPOST = request.POST.copy()
		
		#assert False
		
		i=1
		for index in range(0, int(request.POST["routebase_set-TOTAL_FORMS"])-1):
			if request.POST["routebase_set-" + str(index) + "-base"]:
				newPOST["routebase_set-" + str(index) + "-sequence"]=i
				i += 1
			else:
				newPOST["routebase_set-" + str(index) + "-sequence"] = ""
				
		#assert False
		
		########################################################
		formset = RouteBaseFormset(newPOST, instance=route)
		routeform = RouteForm(request.POST, instance=route)		#only contains the description
		
		if routeform.is_valid() and formset.is_valid():
			route = routeform.save()
			formset = RouteBaseFormset(newPOST, instance=route)
			formset.save()
						
			return HttpResponseRedirect( "/edit/operation/" + str(opbase.operation.pk) )
	
	else:
		if type=="new":
			formset = RouteBaseFormset()
			routeform = RouteForm(instance=route)
		elif type=="edit":	
			formset = RouteBaseFormset(instance=route)
			routeform = RouteForm(instance=route)
		
	return {"type": type, "opbase": opbase, "routeform": routeform, "formset": formset}
	
@login_required()
@render_to('new-edit_operation.html')       
def new_operation(request, pk):
	company = get_object_or_404(Company, pk=pk)

	if request.method == "POST":
		op = Operation(company=company)

		form = OperationForm(request.POST, instance=op)
		if form.is_valid():
			op = form.save()

			formset = OpBaseFormset(request.POST, instance=op)
			if formset.is_valid():
				formset.save()

				return HttpResponseRedirect( "/edit" + company.get_absolute_url() )
	else:
		form = OperationForm(instance=Operation(company=company))
		formset = OpBaseFormset()

	return {'company': company, 'form': form, "formset": formset}
