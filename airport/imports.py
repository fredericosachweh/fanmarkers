import csv, re
from django.contrib.gis.geos import Point
from models import Airport, Region, Country
from psycopg2 import IntegrityError


def ia():   #import airport
    """
id	 "ident"	type	name	latitude_deg	longitude_deg	elevation_ft	continent	iso_country	iso_region	municipality	scheduled_service	gps_code	iata_code	local_code	home_link	wikipedia_link	keywords
    """

    f = open('/home/chris/Desktop/airports.csv', 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    count=0
    count2=0
    count_to = 0

    types = {       '': 0,
                    'balloonport': 7,
                    'closed': 4,
                    'heliport': 5,
                    'large_airport': 3,
                    'medium_airport': 2,
                    'seaplane_base': 6,
                    'small_airport': 1,
            }

    for line in reader:

        throw_out = False
        count += 1
        ##########################

        lat = line["latitude_deg"]
        lng = line["longitude_deg"]

        elev = line["elevation_ft"]

        if elev == "":
            elev=None

        type = line["type"]

        ident = line[' "ident"'].upper()
        name = line["name"]

        country = line["iso_country"].upper()
        city = line["municipality"]
        region = line["iso_region"].upper()

        ##########################

        if ident[:2].upper() == "X-":           ## throw out all closed airports with "X" identifiers
            throw_out = True

        if country == "US":                                     ## US AIRPORTS
            if ident[0] == "K":                             ## STARTS WITH K
                if re.search("[0-9]", ident):           ## HAS NUMBER
                    ident = ident[1:]               ## get rid of the K

        if ident[:3] == "US-":
            ident = ident[3:]                       ## get rid of the "US-" part

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

######################################################################################

def ir():   #import region
    """
    id	code	local_code	name	continent	iso_country	wikipedia_link	keywords
    """

    f = open('/home/chris/Desktop/regions.csv', 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)
    count=0

    for line in reader:
        count += 1

        code = line["code"].upper()
        name = line["name"]
        country = line["iso_country"].upper()

        try:
            Region.objects.get_or_create(name=name, code=code, country=country, )
        except:
            print code

    print "total lines: " + str(count)

######################################################################################

def ic():   #import country
    """
    id	code	name	continent	wikipedia_link	keywords
    """

    f = open('/home/chris/Desktop/countries.csv', 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    count=0

    for line in reader:

        count += 1

        ##########################

        code = line["code"].upper()
        name = line["name"]
        continent = line["continent"].upper()

        try:
            Country.objects.get_or_create(name=name, code=code, continent=continent)
        except:
            print "error: " + code

    print "lines: " + str(count)
