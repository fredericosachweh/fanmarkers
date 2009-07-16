# coding: UTF-8

from django.contrib.auth.decorators import login_required
from main.models import *

from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

from main.immutable_views import *
from main.position_views import *

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
	from forms import CatClassMinsForm, MinsForm, CatClassMinsFormset, OnTypeMinsFormset
	
	position = get_object_or_404(Position, pk=pk)
	
	#############################
	
	if min_type == "Hard":
		mins_object = get_object_or_None(Mins, hard=position)
		if not mins_object:
			mins_object = Mins()

	else:
		mins_object = get_object_or_None(Mins, pref=position)
		if not mins_object:				#if mins object hasnt been created yet, then create it!
			mins_object = Mins()
	
	#############################
	
	mf = MinsForm(instance=mins_object)	
	cat_class_formset = CatClassMinsFormset(instance=mins_object)
	on_type_formset = OnTypeMinsFormset(instance=mins_object)
	
	#assert False
	
	return locals()
	
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


	
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

@login_required()
@render_to('profile.html')
def profile(request):
	from main.forms import ProfileForm, UserForm

	user = request.user
	profile = get_object_or_None(Profile, user=user)
	
	if not profile:
		profile = Profile(user=user)
		
	if request.method == "POST":
		profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
		user_form = UserForm(request.POST, instance=user)
		
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			
			return HttpResponseRedirect( "/" )
	else:
		profile_form = ProfileForm(instance=profile)
		user_form = UserForm(instance=user)
	
	return locals()

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def overlay(request, z, x, y, o):
	from overlay.overlays import GoogleOverlay
	from jobmap.settings import ICONS_DIR
	from django.db.models import Q
	
	just_routes = Airport.route.all()
	all_bases = Airport.base.all()
	
	#layoff = all_bases.filter(layoff__in=Status.objects.all())
	
	all_hiring = Airport.hiring.all()
	not_hiring = Airport.not_hiring.all()
	
	just_hiring = Airport.objects.filter(Q(opbase__choice__in=Status.objects.exclude(advertising=True)) | Q(opbase__assign__in=Status.objects.exclude(advertising=True)))
	advertising = Airport.objects.filter(Q(opbase__choice__in=Status.objects.filter(advertising=True)) | Q(opbase__assign__in=Status.objects.filter(advertising=True)))
	
	##########
	
	if int(z) < 6:
		size = "/small"
	else:
		size = "/big"
	
	ov = GoogleOverlay(z,x,y, queryset=just_routes, field="location")
	ov.icon(ICONS_DIR + size + '/route.png')										# light blue icons for route bases
	
	ov = GoogleOverlay(z,x,y, queryset=all_bases, image=ov.output(shuffle=False), field="location")
	ov.icon(ICONS_DIR + size + '/base.png')										# green icons for no status bases
	
	ov = GoogleOverlay(z,x,y, queryset=all_hiring, image=ov.output(shuffle=False), field="location")		# red for hiring bases
	ov.icon(ICONS_DIR + size + '/hiring.png')
	
	ov = GoogleOverlay(z,x,y, queryset=advertising, image=ov.output(shuffle=False), field="location")		# red-gold for advertising bases
	ov.icon(ICONS_DIR + size + '/advertising.png')
	
	#############################################################

	response = HttpResponse(mimetype="image/png")
	ov.output().save(response, "PNG")
	return response

@render_to('click.html')	
def map_click(request, lat, lng, z):
	from django.contrib.gis.geos import Point
	from django.db.models import Q
	
	point = Point(float(lng), float(lat))	#the point where the user clicked
	
	airport = Airport.relevant.distance(point).order_by('distance')[0]
	
	bases = Position.objects.filter(operation__opbase__in=OpBase.objects.filter(base=airport)).select_related()
	routes = Position.objects.filter(operation__opbase__in=OpBase.objects.filter(route__in=Route.objects.filter(bases=airport))).select_related()
	
	return locals()
	
	
def kml(request, position=None, company=None, airport=None):
	from django.template.loader import get_template
	from django.http import HttpResponse
	from django.template import Context
	
	if position:
		position = get_object_or_404(Position, pk=position)
		routes = Route.objects.filter(opbase__operation__positions=position)
		bases = Airport.objects.filter(opbase__operation__positions=position).distinct()
		
		routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__positions=position).distinct()
		
		title = str(position.company) + " - " + str(position)
	
	if company:
		company = get_object_or_404(Company, pk=company)
		routes = Route.objects.filter(opbase__operation__company=company)
		bases = Airport.objects.filter(opbase__operation__company=company).distinct()
		
		routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__company=company).distinct()
		
		title = str(company)
		
	if airport:
		bases = get_object_or_404(Airport, pk=airport)
		
				
		title = str(airport)  + " - " + str(bases.name)
		
		bases = [bases]
		
	kml = get_template('base.kml').render(Context(locals() ))

	return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")

	
	
	
	
	
	
	
	
	
	
	
