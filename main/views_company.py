from annoying.decorators import render_to
from models import Company
from forms import CompanySearch

@render_to('list_aircraft-company.html')
def make_list(request):

	type="Company"
	
	objects = Company.objects.all()
	
	if request.GET:
	
		searchform = CompanySearch(request.GET)
		
		if searchform.is_valid():

			if int(searchform.cleaned_data["type"]) >= 0:
				objects = objects.filter(type=searchform.cleaned_data["type"])
		
			if int(searchform.cleaned_data["jumpseat"]) >= 0:
				objects = objects.filter(jumpseat=searchform.cleaned_data["jumpseat"])
		 
		 	if searchform.cleaned_data["search"]:
				s = searchform.cleaned_data["search"]
				objects = objects.filter( Q(name__icontains=s) | Q(description__icontains=s) )
				
	else:
		searchform = CompanySearch()

	return locals()
	
def edit(request):
	pass
	
def new(request):
	pass
	
def view(request):
	pass
