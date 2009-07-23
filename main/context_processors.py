from models import *

def google_maps(request):
    from settings import GOOGLE_MAPS_KEY
    return {'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY}

def top_numbers(request):
    from settings import SITE_URL
    from django.db.models import Q

    hiring =        Status.objects.filter( Q(choice_bases__isnull=False) | Q(assign_bases__isnull=False)  ).distinct()
    advertising =   hiring.filter(advertising=True)

    return {"SITE_URL": SITE_URL, 'advertising': "Advertising: " + str(advertising.count()), 'hiring': "Hiring: " + str(hiring.count())}
