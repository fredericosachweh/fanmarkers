import csv, re
from django.contrib.gis.geos import Point
from base.models import Airport, Region, Country
from psycopg2 import IntegrityError 


def ia():
	file = csv.reader(open('/home/chris/Desktop/airports.csv'), "excel")

	count=0
	count2=0
	count_to = 0

	types = {	'': 0,
			'balloonport': 7,
			'closed': 4,
			'heliport': 5,
			'large_airport': 3,
			'medium_airport': 2,
			'seaplane_base': 6,
			'small_airport': 1,
		}

	for line in file:

		throw_out = False
		count += 1
		##########################
	
		lat = line[4]
		lng = line[5]
	
		elev = line[6]
		
		if elev == "":
			elev=None
		
		type = line[2]
	
		ident = line[1].upper()
		name = line[3]
	
		country = line[8].upper()
		city = line[10]
		region = line[9].upper()
	
		##########################
	
		if ident == " \"IDENT\"":
			throw_out = True
	
		if ident[:2].upper() == "X-":		## throw out all closed airports with "X" identifiers
			throw_out = True

		if country == "US":					## US AIRPORTS
			if ident[0] == "K":				## STARTS WITH K
				if re.search("[0-9]", ident):		## HAS NUMBER
					ident = ident[1:]		## get rid of the K
		
		if ident[:3] == "US-":				
			ident = ident[3:]			## get rid of the "US-"	part
			
		if not throw_out:
		
			try:
				Airport.objects.get_or_create(identifier=ident, name=name, region=Region.objects.get(code=region, country=country), municipality=city, country=Country.objects.get(code=country), elevation=elev, location=Point(float(lng), float(lat)), type=types[type])
				count2 += 1
				
			except ValueError:
				print "value - " + ident
				
			except IntegrityError:
				print "integrity - " + ident	
			
		else:
			count_to += 1
			
	print "total:      " + str(count)
	print "success:    " + str(count2)
	print "thrown out: " + str(count_to)
		
def ir():
	file = csv.reader(open('/home/chris/Desktop/regions.csv'), "excel")

	count=0

	for line in file:

		count += 1
	
		##########################
	
		code = line[1].upper()
		name = line[2]
		country = line[4].upper()
	
		if code != "CODE":	
			try:
				Region.objects.get_or_create(name=name, code=code, country=country)
			except:
				print code
	print str(count)

def ic():	
	file = csv.reader(open('/home/chris/Desktop/countries.csv'), "excel")

	count=0

	for line in file:

		count += 1
	
		##########################
	
		code = line[0].upper()
		name = line[1]
	
		if code != "CODE":	
			try:
				Country.objects.get_or_create(name=name, code=code)
			except:
				print code
	print str(count)
