from main.models import *

def google_maps(request):
	from jobmap.settings import GOOGLE_MAPS_KEY
	return {'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY}
	
def top_numbers(request):
	hiring =	Status.objects.exclude(  choice_bases__isnull=True, assign_bases__isnull=True  )
	advertising =	hiring.filter(advertising=True)
	
	return {'advertising': "Advertising: " + str(advertising.count()), 'hiring': "Hiring: " + str(hiring.count())}
	#return {"aa": "aa"}
