from annoying.decorators import render_to
from django.shortcuts import get_object_or_404


from company_tree.models import Company
from models import Aircraft
from forms import AircraftSearch
	
@render_to('view_aircraft.html')
def aircraft(request, pk):

	aircraft = get_object_or_404(Aircraft, pk=pk)
	companies = Company.objects.filter(fleet__aircraft=aircraft)
	
	return locals()
	
@render_to('list_aircraft-company.html')
def make_list(request):

	objects = Aircraft.objects.all()
	type="Aircraft"
	
	if request.GET:
	
		searchform = AircraftSearch(request.GET)
		
		if searchform.is_valid():

			if int(searchform.cleaned_data["cat_class"]) >= 0:
				objects = objects.filter(cat_class=searchform.cleaned_data["cat_class"])
		
			if int(searchform.cleaned_data["engine_type"]) >= 0:
				objects = objects.filter(engine_type=searchform.cleaned_data["engine_type"])
		 
		 	if searchform.cleaned_data["search"]:
				s = searchform.cleaned_data["search"]
				objects = objects.filter( Q(manufacturer__icontains=s) | Q(type__icontains=s) | Q(model__icontains=s) | Q(extra__icontains=s) )
				
	else:
		searchform = AircraftSearch()

	return locals()
	
				
				
				
				
				
				
				
				
				
				
				
				
				

