import Image, ImageFont, ImageDraw, random

from main.models import *
from jobmap.settings import PROJECT_PATH

from django.contrib.gis.gdal.envelope import Envelope
from django.http import HttpResponse

from globalmaptiles import GlobalMercator

class Overlay():

	o = ""
	z = 1
	x = y = 0
		
	gx = gy = ox = oy = 0
	
	gmt = GlobalMercator()
	
	geobase = ""
	
	icon_url = ""
	icon_width = 0
	icon = ""
	
	hard_limit = 100
	
	def __init__(self, z, x, y, o):
		z = int(z)
		x = int(x)
		y = int(y)
		
		self.o = o
		self.z = z
		
		self.x, self.y = x, y
		self.gx, self.gy = x, y
		
		self.ox, self.oy = self.gmt.GoogleTile(x,y,z)						#convert google XY image blocks to some other kind of image block format
		self.N, self.W, self.S, self.E = self.gmt.TileLatLonBounds(self.ox, self.oy, self.z)	#convert this other image block format into lattitude/longitude bound values
		
		self.im = Image.new("RGBA", (256,256))
		#self.im = Image.open(PROJECT_PATH + "/media/myimage.png")
		
	def icon(self, url):
		self.icon = Image.open(url)
		self.icon_width = self.icon.getbbox()[2]
		return self.icon_width
			
	def create_envelope(self):
		res = self.gmt.Resolution(self.z)		#number of meters in one pixel
		rev = res * self.icon_width			#number of meters for half an icon
	
		e_lat, e_long = self.gmt.MetersToLatLon(rev, rev)
	
		ex_W = self.W - e_lat
		ex_E = self.E + e_lat
		ex_S = self.S + e_long
		ex_N = self.N - e_long
	
		return Envelope( (ex_W, ex_N, ex_E, ex_S) )
		
	def shuffle(self):
		bases = list(self.queryset)
		random.shuffle(bases)
		return bases
		
	def put_points(self, bases):
		for base in bases:
			lat = base.location.y
			lng = base.location.x
			
			meters = self.gmt.LatLonToMeters(lat,lng)				#meters from (0,0) to the point
			pixs =   self.gmt.MetersToPixels(meters[0], meters[1], self.z)		#pixels from (0,0) to the point
		
			tx = pixs[0] - (256 * self.ox)						#pixels within this 256x256 image
			ty = pixs[1] - (256 * self.oy)
		
			fx = tx
			fy = 256-ty
		
			x = int(fx - (self.icon_width / 2))		#adjust so the icon is at the center of the point
			y = int(fy - (self.icon_width / 2))
		
			self.place_icon(x,y)
			
	def place_icon(self,x,y):
		self.im.paste(self.icon, (x, y), self.icon)
		
	def output(self):
	
		bounds = self.create_envelope()
		self.geobases = Base.objects.filter(location__intersects=bounds.wkt)[:self.hard_limit]		#get all bases in the square
	
		if(self.icon_width == 0 or self.geobases.count() < 1):		#if no icon is set, of there are no geobases, just return the blank image
			return self.im
				
		self.create_queryset(self.o)
		bases = self.shuffle()
		self.put_points(bases)
		
		self.debug_messages()
		return self.im
		
	def debug_messages(self):
		pass
		#font = ImageFont.load_default()
		#draw = ImageDraw.Draw(self.im)
	
		#draw.text((0, 30), "Hns= " + str(self.S), font=font, fill='black')
		#draw.text((10, 50), "Hew= " + str(self.E), font=font, fill='black')
		#draw.text((0, 70), "Lns= " + str(self.N), font=font, fill='black')	
		#draw.text((10, 90), "Lew= " + str(self.W), font=font, fill='black')
	
		#draw.text((10, 130), "l/l:  x=" + str(bases[0].location.x) + " # y=" + str(bases[0].location.y), font=font, fill='black')
		#draw.text((10, 150), "pix:  x=" + str(x) + " # y=" + str(y), font=font, fill='black')
	
		#draw.text((10, 170), "Z= " + str(self.z), font=font, fill='black')
		#draw.text((10, 150), "BX= " + str(self.ox) + " BY= " + str(self.oy), font=font, fill='black')
		#draw.text((10, 190), "mX= " + str(ax) + " mY= " + str(ay), font=font, fill='black')
		#draw.text((10, 210), "pX= " + str(tilex) + " pY= " + str(tiley), font=font, fill='black')
		#draw.text((10, 230), "C= " + str(self.queryset.count()), font=font, fill='black')
		#draw.text((50, 230), "N= " + str(base), font=font, fill='black')
		#draw.text((50, 210), "Wx=" + str(ex_W), font=font, fill='black')
		#draw.text((50, 230), "Ex=" + str(ex_E), font=font, fill='black')

###################################################################################
###################################################################################
###################################################################################
###################################################################################
		
class BaseOverlay(Overlay):

	def create_queryset(self, filters):
		opbases  = OpBase.objects.filter(base__in=self.geobases)	#get any opbases connected to geobases
		queryset = Base.objects.filter(opbase__in=opbases)		#get all bases connected to those opbases
		self.queryset = queryset
	
	
	
class DestinationOverlay(Overlay):

	def create_queryset(self, filters):
		routebases = RouteBase.objects.filter(base__in=self.geobases)		#get any routebases connected to geobases
		opbases    = OpBase.objects.filter(base__in=self.geobases)		#get any opbases connected to geobases
		
		queryset = Base.objects.filter(routebase__in=routebases)		#get all bases connected to those routebases
		
		if opbases:
			queryset = queryset.exclude(opbase__in=opbases)				#exclude bases that have an opbase
			
		self.queryset = queryset
		
class AllOverlay(Overlay):

	def create_queryset(self, filters):
		self.queryset = self.geobases
		
	
	
def overlay_view(request, z, x, y, o):
	from main.overlays import *
	from jobmap.settings import ICONS_DIR
	       
	if o[0] == "B":
		ov = BaseOverlay(z, x, y, o)				#non-status base
		ov.hard_limit = 10000
	               
		if z<4:		#zoomed out
			ov.icon(ICONS_DIR + '/small/blue.png')
		elif z>=4:	#zoomd in close
			ov.icon(ICONS_DIR + '/big/blue.png')

	#############################################################   

	elif o[0]=="D":							#just a destination
		ov = DestinationOverlay(z, x, y, o)
		ov.hard_limit = 1000
		
		if z<4:		#zoomed out
			ov.icon(ICONS_DIR + '/small/yellow.png')

		elif z>=4:	#zoomd in close
			ov.icon(ICONS_DIR + '/big/yellow.png')
			
	#############################################################
	
	elif o[0]=="H":							#hiring base
		ov = DestinationOverlay(z, x, y, o)
		ov.hard_limit = 1000
		
		if z<4:		#zoomed out
			ov.icon(ICONS_DIR + '/small/yellow.png')

		elif z>=4:	#zoomd in close
			ov.icon(ICONS_DIR + '/big/yellow.png')
			
	#############################################################

	response = HttpResponse(mimetype="image/png")
	ov.output().save(response, "PNG")
	return response
		

