from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from django.views.generic.create_update import update_object, create_object
from django.db.models import Q

from main.models import Company

from forms import AircraftForm, AircraftSearch
from models import Aircraft

################################

@render_to('view_aircraft.html')
def view(request, pk):
    aircraft = get_object_or_404(Aircraft, pk=pk)
    companies = Company.objects.filter(fleet__aircraft=aircraft)
    return locals()

def edit(request, pk):
    return update_object(request, object_id=pk, form_class=AircraftForm, template_name="new-edit_aircraft.html")

def new(request):
    return create_object(request, form_class=AircraftForm, template_name="new-edit_aircraft.html")

@render_to('list_aircraft-company.html')
def make_list(request):
    objects = Aircraft.objects.all()
    type="Aircraft"
    if request.GET.get("cat_class", False):
        searchform = AircraftSearch(request.GET)
        searchform.is_valid()

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
