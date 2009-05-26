# coding: UTF-8

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import *

def jobmap(request):
	c = RequestContext(request)
	return render_to_response('map.html', c )
	
def company(request, company_id):

	company=""
	fail=""

	try:
		company = Company.objects.select_related().get(pk=company_id)
	except:
		fail=True

	c = RequestContext(request, {'c': company, "not_found": fail} )
	return render_to_response('company.html', c )
	
def company_master_list(request):

	companies = Company.objects.all()[:50]				# get the first 50 companies
	
	c = RequestContext(request, {'companies': companies} )
	return render_to_response('company_master_list.html', c )
	
def airport(request, airport_id):

	airport=""
	fail=""

	try:
		airport = Base.objects.select_related().get(pk=airport_id)
	except:
		c = RequestContext(request, {"not_found": True} )
		return render_to_response('airport.html', c )
		
	###################
	ops_base = []
	ops_fly = []
	
	op_based = 	Operation.objects.filter(opbase__in=OpBase.objects.filter(base=airport))
	op_fly =	Operation.objects.filter(opbase__in=OpBase.objects.filter(routes__in=Route.objects.filter(bases=airport)))
	
	
	for op in op_based:
		ops_base.append(op)
		
	for op in op_fly:
		ops_fly.append(op)
	
	
	c = RequestContext(request, {'a': airport, "ops_base": ops_base, "ops_fly": ops_fly, "not_found": fail} )
	return render_to_response('airport.html', c )
	
def data_import(request):
	
	c = RequestContext(request, {'c': company} )
	return render_to_response('company.html', c )
	
def overlay(request, zoom, x, y):
	import Image, ImageFont, ImageDraw
	from globalmaptiles import *
	
	gmt = GlobalMercator()
	coords = gmt.TileLatLonBounds(int(x), int(y), int(zoom))
	
	font = ImageFont.load_default()
	
	im = Image.open("/home/chris/Websites/jobmap/media/myimage.png")
	#im = Image.new("RGB", (256,256), "green")
	
	#points = Base.objects.filter(lat__gte=str(coords[0])).filter(lat__lte=str(coords[2])).filter(long__gte=str(coords[1])).filter(long__lte=str(coords[3]))
	#count = points.count()
	
	draw = ImageDraw.Draw(im)
	draw.text((10, 10), "lats:     (" + str(coords[0]) + ", " + str(coords[2])+")", font=font)
	draw.text((10, 30), "longs:    (" + str(coords[1]) + ", " + str(coords[3])+")", font=font)
	draw.text((10, 50), "zoom:      " + str(zoom), font=font)
	draw.text((10, 70), "quadtree:  " + str(x) + " # " + str(y), font=font)
	#draw.text((10, 90), "points:    " + str(count), font=font)
	
	if zoom==0 or zoom==1:
		marker_size = 1
	if zoom==2 or zoom==3:
		marker_size = 2

	response = HttpResponse(mimetype="image/png")
	im.save(response, "PNG")
	return response

	
	
	
	
	
	
	
	
	
	
