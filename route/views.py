from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

from models import *
from forms import *

@login_required()
@render_to('new-edit_route.html')
def handle_route(request, pk, type):
	from forms import RouteBaseFormset, RouteForm

	if type=="new":
		opbase = get_object_or_404(OpBase, pk=pk)
		route = Route(home=opbase)
	elif type=="edit":
		route = get_object_or_404(Route, pk=pk)
		opbase = route.home
		
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
						
			return HttpResponseRedirect( opbase.operation.get_edit_url() )
	
	else:
		if type=="new":
			formset = RouteBaseFormset()
			routeform = RouteForm(instance=route)
		elif type=="edit":	
			formset = RouteBaseFormset(instance=route)
			routeform = RouteForm(instance=route)
		
	return locals()
	
def edit(request, pk=0):
	aa = "aa"
	return locals()
