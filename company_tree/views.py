from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.db.models import Q

from models import *
from forms import *

###############################################################################

@login_required()
@render_to('new-edit_operation.html')		
def edit_operation(request, pk):


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

@login_required()
@render_to('new-edit_fleet.html')	
def new_fleet(request, pk):

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
@render_to('profile.html')
def profile(request):
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

	
	
	
	
	
	
	
	
	
	
	
