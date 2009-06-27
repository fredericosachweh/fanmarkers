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
	from django.db.models import Q
	
	usa_bases = Base.objects.filter(country__exact="United States")
	
	all_hiring = Position.objects.exclude(status__choice_bases__isnull=True, status__assign_bases__isnull=True).values('pk')
	just_hiring = all_hiring.exclude(status__advertising=True)
	advertising = all_hiring.filter(status__advertising=True)
	layoff = Status.objects.filter(layoff_bases__isnull=False).values('pk')
	
	usa_h = Status.objects.filter(   Q(assign_bases__in=usa_bases) | Q(choice_bases__in=usa_bases)    ).count()

	return {"usa_h": usa_h}

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
@render_to('new-edit_operation.html')		
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


	return {'operation': op, 'form': form, 'formset': formset, "type": "edit"}

###############################################################################
	
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
@render_to('new-edit_fleet.html')	
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
		
	return {'company': company, 'form': form, "type": "new"}
	
###############################################################################	

@login_required()
@render_to('new-edit_route.html')
def handle_route(request, type, pk):
	from forms import RouteBaseFormset, RouteForm

	if type=="new":
		opbase = get_object_or_404(OpBase, pk=pk)
		route = Route(opbase=opbase)
	elif type=="edit":
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
	from forms import OperationForm, OpBaseFormset
	from django.forms.models import inlineformset_factory

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


#############################################################################################################################
#############################################################################################################################
#from main.overlays import overlay_view
#############################################################################################################################
#############################################################################################################################

@login_required()
@render_to('edit_status.html')		
def edit_status(request, pk):
	from forms import StatusForm, newBase
	import datetime

	newbases = []
	
	position = get_object_or_404(Position, pk=pk)
	operation = Operation.objects.get(positions=position)
	opbases = operation.opbase_set.all()
	bases = Base.objects.filter(opbase__in=opbases)
	
	status = get_object_or_None(Status, position=position)
	
	#status = Status.objects.select_related().get(position=position)
	
	if not status:
		status = Status(position=position)
	
	if request.method == "POST":
		
		newPOST = request.POST.copy()
		newPOST.update({"position": position.pk})
		
		field_bases = {}
		field_bases["not"] = field_bases["assign"] = field_bases["choice"] = field_bases["layoff"] = []
		
		for base in bases:
			for item in ("not", "assign", "choice", "layoff", ):
				if newPOST[str(base)] == item:
					field_bases[item] = field_bases[item] + [base]
		#assert False			
					
		form = StatusForm(newPOST, instance=status)
		if form.is_valid():
			instance = form.save()
			instance.not_bases = field_bases["not"]
			instance.assign_bases = field_bases["assign"]
			instance.choice_bases = field_bases["choice"]
			instance.layoff_bases = field_bases["layoff"]
			instance.save()
			
		return HttpResponseRedirect( "/edit" + position.get_absolute_url() )
	else:
		for base in bases:
			newbase = newBase()
			newbase.identifier = base.identifier
			newbase.location_summary = base.location_summary
			
			if not status.pk:
				newbase.unknown_checked = 'checked="checked"'
				
			elif base in status.not_bases.all():
				newbase.not_checked = 'checked="checked"'
				
			elif base in status.choice_bases.all():
				newbase.choice_checked = 'checked="checked"'
				
			elif base in status.assign_bases.all():
				newbase.assign_checked = 'checked="checked"'
				
			elif base in status.layoff_bases.all():
				newbase.layoff_checked = 'checked="checked"'
				
			else:
				newbase.unknown_checked = 'checked="checked"'
			
			newbases.append(newbase)
			
		form = StatusForm()
	
	return {"bases": newbases, "form": form, "position": position, "last_modified": status.last_modified}
	
#############################################################################################################################
		
@login_required()
@render_to('edit_salary.html')	
def edit_salary(request, pk):
	from main.forms import CompensationForm, PayscaleFormset
	
	position = get_object_or_404(Position, pk=pk)
	comp = get_object_or_None(Compensation, position=position)
	
	if not comp:
		comp = Compensation(position=position)
	
	
	
	if request.method == "POST":
		form = CompensationForm(request.POST, instance=comp)
		#form.save()
	else:
		form = CompensationForm(instance=comp)
		formset = PayscaleFormset(instance=comp)
	
	return {"form": form, "formset": formset, "position": position}

#############################################################################################################################

@login_required()
@render_to('profile.html')
def profile(request):
	from main.forms import ProfileForm, UserForm

	user = request.user
	profile = get_object_or_None(Profile, user=user)
	
	if not profile:
		profile = Profile(user=user)
		
	if request.method == "POST":
		profile_form = ProfileForm(request.POST, instance=profile)
		user_form = UserForm(request.POST, instance=user)
		
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			
			return HttpResponseRedirect( "/" )
	else:
		profile_form = ProfileForm(instance=profile)
		user_form = UserForm(instance=user)
	
	return locals()



def overlay(request, z, x, y, o):
	from overlay.overlay_class import OverlayClass
	from jobmap.settings import ICONS_DIR
	from django.db.models import Q
	
	#bases
	layoff = Base.objects.filter(layoff__in=Status.objects.all())
	all_hiring = Base.objects.filter(Q(choice__in=Status.objects.all()) | Q(assign__in=Status.objects.all()))
	just_hiring = Base.objects.filter(Q(choice__in=Status.objects.exclude(advertising=True).values('pk')) | Q(assign__in=Status.objects.exclude(advertising=True).values('pk')))
	advertising = Base.objects.filter(Q(choice__in=Status.objects.filter(advertising=True).values('pk')) | Q(assign__in=Status.objects.filter(advertising=True).values('pk')))
	
	ov = OverlayClass(x=x,y=y,z=z, queryset=all_hiring)
	ov.icon(ICONS_DIR + '/small/red.png')
		
	#############################################################

	response = HttpResponse(mimetype="image/png")
	ov.output().save(response, "PNG")
	return response	

	
			
	
	
