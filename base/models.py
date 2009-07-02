from django.contrib.gis.db import models
from django.contrib.auth.models import User
from main.constants import AIRPORT_TYPE

class Airport(models.Model):
	identifier	=	models.CharField(max_length=8, primary_key=True)
	
	name		=	models.CharField(max_length=96)
	municipality	=	models.CharField(max_length=60)
	country		=	models.ForeignKey("Country")
	region		=	models.ForeignKey("Region")
	type		=	models.IntegerField(choices=AIRPORT_TYPE)
	
	elevation	=	models.IntegerField(null=True)
	location	=	models.PointField()
	
	watchers	=	models.ManyToManyField(User, blank=True, )
	
	objects		=	models.GeoManager()
	
	class Meta:
		ordering = ["identifier", "country"]
		verbose_name_plural = "Bases"
		
	def get_absolute_url(self):
		return "/airport/%s/" % (self.identifier, )
		
	def __unicode__(self):
		return u"%s" % (self.identifier,)
		
	def display_name(self):
		return " - ".join([self.identifier, self.name])

	def location_summary(self):
		ret = []
		
		for item in (self.municipality, self.region.code, self.country.code, ):
			if item and item != "US":
				ret.append(item)
				
		return ", ".join(ret)
		
class Region(models.Model):
	code = models.CharField(max_length=48)
	country = models.CharField(max_length=2)
	name = models.CharField(max_length=60)
	
	def __unicode__(self):
		return "%s - %s" % (self.country.name, self.name)
	
class Country(models.Model):
	name = models.CharField(max_length=48)
	code = models.CharField(max_length=2, primary_key=True)
	
	def __unicode__(self):
		return self.name
