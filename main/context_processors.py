from models import *

def settings_values(request):
    from django.conf import settings 
    return {"SITE_URL": settings.SITE_URL,
            "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY}

def top_numbers(request):
    from settings import SITE_URL
    from django.db.models import Q

    hiring =        Status.objects.filter(
                        Q(choice_bases__isnull=False)
                      | Q(assign_bases__isnull=False)
                    ).distinct()
                    
    advertising =   hiring.filter(advertising=True)

    return {
            'advertising': "Advertising: %s" % advertising.count(),
            'hiring': "Hiring: %s" % hiring.count()
           }
