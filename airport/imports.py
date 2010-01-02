import csv
import re

from psycopg2 import IntegrityError

from django.contrib.gis.geos import Point

from airport.models import Airport, Region, Country


def ia():
    f = csv.reader(open('airport/fixtures/airports.csv'), "excel")
    f.next() # skip the header line
    
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

    for line in f:

        throw_out = False
        count += 1
        ##########################
        
        pk = line[0]
        
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

        if ident[:2].upper() == "X-":           ## throw out all closed airports with "X" identifiers
            throw_out = True

        if country == "US":                                     ## US AIRPORTS
            if ident[0] == "K":                             ## STARTS WITH K
                if re.search("[0-9]", ident):           ## HAS NUMBER
                    ident = ident[1:]               ## get rid of the K

        if ident[:3] == "US-":
            ident = ident[3:]                       ## get rid of the "US-" part

        if not throw_out:
            region = Region.objects.get(code=region, country=country)
            country = Country.objects.get(code=country)
            try:
                Airport.objects.get_or_create(
                          pk=pk,
                          identifier=ident,
                          name=name,
                          region=region,
                          municipality=city,
                          country=country,
                          elevation=elev,
                          location='POINT (%s %s)' % (lng, lat),
                          type=types[type]
                )
                
                count2 += 1

            except Exception, e:
                print ident, e
            else:
                count_to += 1

    print "total:      " + str(count)
    print "success:    " + str(count2)
    print "thrown out: " + str(count_to)


def ir():
    f = csv.reader(open('airport/fixtures/regions.csv'), "excel")
    f.next()
    count=0

    for line in f:

        ##########################

        code = line[1].upper()     # the full code, eg: "US-PA"
        name = line[3]             # human readable name "Delaware"
        country = line[5].upper()  # country name, eg: "United States"

        try:
            Region.objects.get_or_create(
                    name=name,
                    code=code,
                    country=country
            )
        except Exception, e:
            print code, e
        else:
            count += 1
                
    print "--------\ntotal success: %s" % count


def ic():
    f = csv.reader(open('airport/fixtures/countries.csv'), "excel")
    f.next()
    count=0

    for line in f:

        ##########################

        code = line[1].upper()
        name = line[2]


        try:
            print name, code
            Country.objects.get_or_create(name=name, code=code)
        except Exception, e:
            print code, e
        else:
            count += 1
            
    print "--------\ntotal success: %s" % count









