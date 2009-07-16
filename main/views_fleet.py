from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.create_update import update_object, create_object
from forms import FleetForm
	
def edit(request, pk):
	return update_object(request, object_id=pk, form_class=FleetForm, template_name='new-edit_fleet.html')

@login_required()
@render_to('new-edit_fleet.html')	
def new(request, pk):
	company = get_object_or_404(Company, pk=pk)
	type="new"

	if request.method == "POST":
		fleet = Fleet(company=company)
		form = FleetForm(request.POST, instance=fleet)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( company.get_edit_url() )
	else:
		form = FleetForm()
		
	return locals()
