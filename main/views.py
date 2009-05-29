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
	
def overlay(request, zoom, x, y):
	import Image, ImageFont, ImageDraw
	from globalmaptiles import GlobalMercator, GlobalGeodetic
	from django.contrib.gis.geos import Point, LinearRing
	from jobmap.settings import PROJECT_PATH
	from django.contrib.gis.gdal.envelope import Envelope
	import random
	
	ox, oy = x,y
	
	gmt = GlobalMercator()
	gx,gy = gmt.GoogleTile(int(x), int(y), int(zoom))			#convert google XY image blocks to some other kind of image block format
	W, N, E, S = gmt.TileLatLonBounds(int(gx), int(gy), int(zoom))		#convert this other image block format into lattitude/longitude bound values
	bounds = Envelope((N + (N * (.01)), W + (W * (.01)), S + (S * (.01)), E + (E * (.01)), ))
	#bounds = Envelope((N,W,S,E))
	bases = list(Base.objects.filter(location__intersects=bounds.wkt)[:500])
	random.shuffle(bases)
	
	im = Image.new("RGBA", (256,256))
	#im =   Image.open(PROJECT_PATH + "/media/myimage.png")
	font = ImageFont.load_default()
	draw = ImageDraw.Draw(im)

	icon = Image.open(PROJECT_PATH + "/media/icons/small_red.png")
	
	if zoom<5:
		icon = Image.open(PROJECT_PATH + "/media/icons/small_red.png")
	if zoom>5:
		icon = Image.open(PROJECT_PATH + "/media/icons/big_red.png")
	
	for base in bases:
		lat = base.location.x
		lng = base.location.y
		
		y = (lng - E) / (W - E) * 256
		x = (lat - S) / (N - S) * 256
		
		im.paste(icon, (256-x, y), icon)
		
	#draw.text((10, 30), "W= " + str(W), font=font, fill='black')	
	#draw.text((10, 50), "N= " + str(N), font=font, fill='black')
	#draw.text((10, 70), "E= " + str(E), font=font, fill='black')
	#draw.text((10, 90), "S= " + str(S), font=font, fill='black')
	#draw.text((10, 130), "l/l:  x=" + str(bases[0].location.x) + " # y=" + str(bases[0].location.y), font=font, fill='black')
	#draw.text((10, 150), "pix:  x=" + str(x) + " # y=" + str(y), font=font, fill='black')
	
	#draw.text((10, 170), "Z= " + str(zoom), font=font, fill='black')
	#draw.text((10, 190), "BX= " + str(ox) + " BY= " + str(oy), font=font, fill='black')
	#draw.text((10, 230), "C= " + str(count), font=font, fill='black')
	
	

	response = HttpResponse(mimetype="image/png")
	im.save(response, "PNG")
	return response

	
	
	
	
	
	
	
	
	
	
