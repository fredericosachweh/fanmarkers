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
	
def edit_company(request, company_id):
	from forms import CompanyForm
	
	company = Company.objects.get(pk=company_id)
	company_form = CompanyForm(instance=company)
	
	operations = []
	
	for op in company.operation_set.all():
		operations.append(op)
	
	c = RequestContext(request, {'c': company, 'company_form': company_form, 'operations': operations} )
	return render_to_response('company_edit.html', c )
	
def edit_operation(request, op_id):
	from forms import OpBaseForm
	from django.forms.models import modelformset_factory

	OpBaseFormSet = modelformset_factory(OpBase, form=OpBaseForm)
	op = Operation.objects.get(pk=op_id)
	formset = OpBaseFormSet(queryset=op.opbase_set.all())

	c = RequestContext(request, {'operation': op, 'formset': formset} )
	return render_to_response('operation_edit.html', c )
	
def overlay(request, z, x, y, o):
	import Image, ImageFont, ImageDraw
	from globalmaptiles import GlobalMercator, GlobalGeodetic
	from django.contrib.gis.geos import Point, LinearRing
	from jobmap.settings import PROJECT_PATH
	from django.contrib.gis.gdal.envelope import Envelope
	import random
	
	##############################################################################################
	
	z = int(z)
	x,y = int(x), int(y)
	
	##############################################################################################
	ox, oy = x,y
	
	gmt = GlobalMercator()
	gx,gy = gmt.GoogleTile(x,y, z)				#convert google XY image blocks to some other kind of image block format
	N, W, S, E = gmt.TileLatLonBounds(gx, gy, z)		#convert this other image block format into lattitude/longitude bound values
	
	#############################################################################################
	
	if z<4:									#zoomed out
		base_icon = Image.open(PROJECT_PATH + "/media/icons/small_blue.png")
		dest_icon = Image.open(PROJECT_PATH + "/media/icons/small_red.png")
		iwidth = 8
		
	elif z>=4:									#zoomd in close
		base_icon = Image.open(PROJECT_PATH + "/media/icons/big_red.png")
		dest_icon = Image.open(PROJECT_PATH + "/media/icons/big_blue.png")
		iwidth = 16
	
	##############################################################################################
	
	res = gmt.Resolution(z)		#number of meters in one pixel
	rev = res * iwidth			#number of meters for half an icon
	
	e_lat, e_long = gmt.MetersToLatLon(rev, rev)
	
	ex_W = W - e_lat
	ex_E = E + e_lat
	ex_S = S + e_long
	ex_N = N - e_long
	
	bounds = Envelope( (ex_W, ex_N, ex_E, ex_S) )

	##############################################################################################
	##############################################################################################
	
	geobases = Base.objects.filter(location__intersects=bounds.wkt)			#get all bases in the square
	
	if o[0] == 'B':		#base airport layer
		opbases = OpBase.objects.filter(base__in=geobases)		#get any opbases connected to geobases
		queryset = Base.objects.filter(opbase__in=opbases)		#get all bases connected to those opbases
		
		icon = base_icon

	
	elif o[0] == 'D':	#destinations
		routebases = RouteBase.objects.filter(base__in=geobases)		#get any routebases connected to geobases
		opbases = OpBase.objects.filter(base__in=geobases)			#get any opbases connected to geobases
		
		queryset = Base.objects.filter(routebase__in=routebases)		#get all bases connected to those routebases
		if opbases:
			queryset = queryset.exclude(opbase__in=opbases)				#exclude bases that have an opbase
			
		icon = dest_icon
		
		
	##############################################################################################

	bases = list(queryset[:100])
	random.shuffle(bases)

	##############################################################################################
	
	im = Image.new("RGBA", (256,256))
	#im =   Image.open(PROJECT_PATH + "/media/myimage.png")
	font = ImageFont.load_default()
	draw = ImageDraw.Draw(im)
	
	##############################################################################################
	
	for base in bases:
		lat = base.location.y
		lng = base.location.x
			
		meters = gmt.LatLonToMeters(lat,lng)				#meters from (0,0) to the point
		pixs = gmt.MetersToPixels(meters[0], meters[1], z)		#pixels from (0,0) to the point
		
		tx = pixs[0] - (256 * gx)						#pixels within this 256x256 image
		ty = pixs[1] - (256 * gy)
		
		fx = tx
		fy = 256-ty
		
		ax = int(fx - (iwidth / 2))		#adjust so the icon is at the center of the point
		ay = int(fy - (iwidth / 2))
		
		im.paste(icon, (ax, ay), icon)
		
	#draw.text((0, 30), "Hns= " + str(S) + "= " + str(Ss), font=font, fill='black')
	#draw.text((10, 50), "Hew= " + str(E) + "= " + str(Es), font=font, fill='black')
	#draw.text((0, 70), "Lns= " + str(N) + "= " + str(Ns), font=font, fill='black')	
	#draw.text((10, 70), "Lew= " + str(W) + "= " + str(Ws), font=font, fill='black')
	
	#draw.text((10, 130), "l/l:  x=" + str(bases[0].location.x) + " # y=" + str(bases[0].location.y), font=font, fill='black')
	#draw.text((10, 150), "pix:  x=" + str(x) + " # y=" + str(y), font=font, fill='black')
	
	#draw.text((10, 170), "Z= " + str(z), font=font, fill='black')
	#draw.text((10, 150), "BX= " + str(ox) + " BY= " + str(oy), font=font, fill='black')
	#draw.text((10, 190), "mX= " + str(ax) + " mY= " + str(ay), font=font, fill='black')
	#draw.text((10, 210), "pX= " + str(tilex) + " pY= " + str(tiley), font=font, fill='black')
	#draw.text((10, 230), "C= " + str(count), font=font, fill='black')
	#draw.text((50, 230), "N= " + str(base), font=font, fill='black')
	#draw.text((50, 210), "Wx=" + str(ex_W), font=font, fill='black')
	#draw.text((50, 230), "Ex=" + str(ex_E), font=font, fill='black')

	response = HttpResponse(mimetype="image/png")
	im.save(response, "PNG")
	return response

	
	
	
	
	
	
	
	
	
	
