from main.models import *

def titles(request):
	return {'site_name': "FlightJobb.in", 'tagline': "map of jobs", "domain": "flightjobb.in"}
	
def top_numbers(request):
	#hiring =	OpBase.objects.filter(hiring_status=2).count()
	#advertising =	OpBase.objects.filter(hiring_status=3).count()
	#return {'advertising': str(advertising), 'hiring': str(hiring)}
	return {"dd": "SS"}
