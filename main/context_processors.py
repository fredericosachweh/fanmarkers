from main.models import *

def google_maps(request):
	from jobmap.settings import GOOGLE_MAPS_KEY
	return {'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY}
	
def top_numbers(request):
	#hiring =	OpBase.objects.filter(hiring_status=2).count()
	#advertising =	OpBase.objects.filter(hiring_status=3).count()
	
	hiring = "??"
	advertising = "??"
	
	return {'advertising': str(advertising), 'hiring': str(hiring)}
