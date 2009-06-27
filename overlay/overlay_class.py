import Image, ImageFont, ImageDraw, random

from main.models import *
from jobmap.settings import PROJECT_PATH

from django.contrib.gis.gdal.envelope import Envelope
from django.http import HttpResponse

from globalmaptiles import GlobalMercator

class OverlayClass():

	gmt = GlobalMercator()
	hard_limit = 100
	
	def __init__(self, z=1, x=1, y=1, o="", image="", queryset="", pointfield=True):
		z = int(z)
		x = int(x)
		y = int(y)
		
		self.options = o
		self.zoom = z
		self.queryset = queryset
		self.pointfield = pointfield
		
		if image == "":
			self.im = Image.new("RGBA", (256,256))
			#self.im = Image.open(PROJECT_PATH + "/media/test.png")
		else:
			self.im = image
		
		self.x, self.y = x, y
		self.gx, self.gy = x, y
		
		self.ox, self.oy = self.gmt.GoogleTile(x,y,z)						#convert google XY image blocks to some other kind of image block format
		self.N, self.W, self.S, self.E = self.gmt.TileLatLonBounds(self.ox, self.oy, self.zoom)	#convert this other image block format into lattitude/longitude bound values
			
	def icon(self, path):
		self.icon = Image.open(path)
		self.icon_width = self.icon.getbbox()[2]
		return self.icon_width
			
	def create_envelope(self):
		"""Creates an envelope with the bounds being the lattitude/longitude of the image.
		It also extends the bounds by half the width of the icon used so any icons that are placed
		near the edges of any image will not get cut off
		"""
		
		res = self.gmt.Resolution(self.zoom)		#number of meters in one pixel
		rev = res * self.icon_width			#number of meters for half an icon

		e_lat, e_long = self.gmt.MetersToLatLon(rev, rev)

		ex_W = self.W - e_lat
		ex_E = self.E + e_lat
		ex_S = self.S + e_long
		ex_N = self.N - e_long
		
		if self.pointfield:
			return Envelope( (ex_W, ex_N, ex_E, ex_S) )
		else:
			return (ex_W, ex_N, ex_E, ex_S)
		
	def shuffle(self):
		bases = list(self.queryset)
		random.shuffle(bases)
		return bases
		
	def put_points(self):
		for base in self.geobases:
			lat = base.location.y
			lng = base.location.x
			
			meters = self.gmt.LatLonToMeters(lat,lng)				#meters from (0,0) to the point
			pixs =   self.gmt.MetersToPixels(meters[0], meters[1], self.zoom)		#pixels from (0,0) to the point
		
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
		
		if self.pointfield:
			self.geobases = self.queryset.filter(location__intersects=bounds.wkt)[:self.hard_limit]
		else:
			self.geobases = self.queryset.filter(location__intersects=bounds.wkt)[:self.hard_limit]
			
		geobases = self.geobases
	
		if self.icon_width == 0 or self.geobases.count() < 1:		#if no icon is set, or there are no geobases, just return the unmodified original image
			return self.im
				
		self.put_points()
		
		#self.debug_messages()
		
		return self.im
		
	def debug_messages(self):
		#pass
		font = ImageFont.load_default()
		draw = ImageDraw.Draw(self.im)

		draw.text((10, 150), "pix:  z=" + str(self.zoom) + " x=" + str(self.x) + " # y=" + str(self.y), font=font, fill='black')
		draw.text((10, 230), "Geo= " + str(self.geobases.count()), font=font, fill='black')
		draw.text((10, 210), "Org= " + str(self.queryset.count()), font=font, fill='black')

###################################################################################
###################################################################################
###################################################################################
###################################################################################
