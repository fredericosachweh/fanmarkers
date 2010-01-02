from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from models import *
from company.models import Company
from operation.models import Operation

################################

@render_to('view_airport.html')
def airport(request, ident):

    airport = get_object_or_404(Airport, identifier=ident)

    #ops where this airport is a base
    company_base =  Company.objects\
                           .filter(operation__opbase__base=airport)\
                           .distinct()
    
    #ops where this airport is part of a route                    
    ops_fly =       Operation.objects\
                             .filter(opbase__route__bases=airport)\
                             .distinct()

    kmz_url = reverse("kml-airport", kwargs={"ident": ident})

    return locals()

def kmz(request, ident):

    base = Airport.goon(identifier=ident)
    title = "%s - %s" % (ident, base.name)
    #make it a list so it can be iterated in the template
    bases = [base]
    
    from kml.utils import locals_to_kmz_response
    return locals_to_kmz_response(locals())
