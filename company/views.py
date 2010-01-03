from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from annoying.decorators import render_to

from models import Company
from forms import CompanySearch, CompanyForm

@render_to('list_aircraft-company.html')
def make_list(request):
    type="Company"
    objects = Company.objects.all()

    if request.GET.get("type", False):

        searchform = CompanySearch(request.GET)
        searchform.is_valid()

        if int(searchform.cleaned_data["type"]) >= 0:
            ty = searchform.cleaned_data["type"]
            objects = objects.filter(type=ty)

        if int(searchform.cleaned_data["jumpseat"]) >= 0:
            js = searchform.cleaned_data["jumpseat"]
            objects = objects.filter(jumpseat=js)

        if searchform.cleaned_data["search"]:
            s = searchform.cleaned_data["search"]
            objects = objects.filter(   Q(name__icontains=s)
                                      | Q(description__icontains=s)
                                    )
    else:
        searchform = CompanySearch()

    return locals()

########################################################

@login_required()
def edit(request, pk):
    from django.views.generic.create_update import update_object
    return update_object(
                            request,
                            object_id=pk,
                            form_class=CompanyForm,
                            template_name='edit_company.html'
                        )

@login_required()
def new(request):
    from django.views.generic.create_update import create_object
    return create_object(
                            request,
                            form_class=CompanyForm,
                            template_name='new_company.html',
                         )

@render_to('view_company.html')
def view(request, pk, slug):
    company = Company.goof(pk=pk)

    if not company.slug == slug:
        return HttpResponseRedirect(company.get_absolute_url() )

    kmz_url = reverse("kml-company", kwargs={"pk": company.pk})

    return locals()

def kml(request, pk):
    
    from route.models import Route
    from airport.models import Airport
   
    company = Company.goof(pk=pk)
    
    routes = Route.objects.filter(home__operation__company=company)
    bases = Airport.objects\
                   .filter(opbase__operation__company=company)\
                   .distinct()
                   
    routebases = Airport.objects\
                        .filter(routebase__route__in=routes)\
                        .exclude(opbase__operation__company=company)\
                        .distinct()
                        
    title = str(company)
    
    print company
    
    from kml.utils import locals_to_kmz_response    
    return locals_to_kmz_response(locals())





