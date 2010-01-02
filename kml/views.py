







def kml(request, position=None, company=None, airport=None):
    from django.template.loader import get_template
    from django.http import HttpResponse
    from django.template import Context
    from route.models import Route
    from settings import MEDIA_URL

    MEDIA_URL = MEDIA_URL

    if position:
        position = get_object_or_404(Position, pk=position)
        routes = Route.objects.filter(home__operation__positions=position)
        bases = Airport.objects.filter(opbase__operation__positions=position).distinct()
        routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__positions=position).distinct()
        title = str(position.company) + " - " + str(position)

    if company:
        company = get_object_or_404(Company, pk=company)
        routes = Route.objects.filter(home__operation__company=company)
        bases = Airport.objects.filter(opbase__operation__company=company).distinct()
        routebases = Airport.objects.filter(routebase__route__in=routes).exclude(opbase__operation__company=company).distinct()
        title = str(company)

    if airport:
        base = get_object_or_404(Airport, identifier=airport)
        title = "%s - %s" % (airport, base.name)
        #make it a list so it can be iterated in the template
        bases = [base]
    
    from utils import locals_to_kmz_response
    return locals_to_kmz_response(locals())
