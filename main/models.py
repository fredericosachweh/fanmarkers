from django.contrib.gis.db import models
from django.contrib.auth.models import User
from constants import *
from mins import Mins

class Aircraft(models.Model):
	model		=	models.CharField(max_length=64, blank=True)
	type		=	models.CharField(max_length=32)
	extra		=	models.CharField(max_length=32, blank=True)
	manufacturer	=	models.CharField(max_length=32)
	engine_type	=	models.IntegerField(choices=ENGINE_TYPE, default=0)
	cat_class	=	models.IntegerField(choices=CAT_CLASSES, default=1)	
	
	def __unicode__(self):
		ret=[]
		if self.manufacturer:
			ret.append(self.manufacturer)
			
		ret.append(self.type)
		
		if self.model:
			ret.append(self.model)
			
		return " - ".join(ret)
		
class PayscaleYear(models.Model):
	company		=	models.ForeignKey("Company")
	position	=	models.ForeignKey("Position")
	year		=	models.IntegerField()
	amount		=	models.FloatField()
	salary_unit	=	models.IntegerField(choices=SALARY_TYPE)
	
class Base(models.Model):
	identifier	=	models.CharField(max_length=8, primary_key=True)
	local		=	models.CharField(max_length=8)
	iata		=	models.CharField(max_length=8)
	
	name		=	models.CharField(max_length=96)
	municipality	=	models.CharField(max_length=60)
	country		=	models.CharField(max_length=48)
	region		=	models.CharField(max_length=48)
	type		=	models.IntegerField(choices=AIRPORT_TYPE)
	
	elevation	=	models.IntegerField()
	location	=	models.PointField()
	
	objects		=	models.GeoManager()
	
	class Meta:
		ordering = ["city", "sector"]
		
	def display_name(self):
		ret = self.identifier
		if len(self.name) > 0:
			ret = ret + " - " + self.name
			
		return ret
		
	class Meta:
        	verbose_name_plural = "Bases"

		
	def __unicode__(self):
		return u"%s" % (self.identifier,)
		
class Route(models.Model):
	bases		=	models.ManyToManyField("Base", through="RouteBase", blank=True)
	description	=	models.TextField(blank=True)

class RouteBase(models.Model):
	bases		=	models.ForeignKey("Base")
	route		=	models.ForeignKey("Route")
	sequency	=	models.IntegerField()
		
	
class Fleet(models.Model):
	company		=	models.ForeignKey("Company")
	aircraft	=	models.ForeignKey("Aircraft")
	size		=	models.IntegerField(default=1)
	description	=	models.TextField(blank=True)
	
	def __unicode__(self):
		return u"%s - %s" % (self.aircraft.model, self.company.name)

class Company(models.Model):
	name		=	models.CharField(max_length=64)
	call_sign	=	models.CharField(max_length=32, blank=True)
	website		=	models.URLField(blank=True)
	description	=	models.TextField(blank=True)
	type		=	models.IntegerField(choices=BUSINESS_TYPE, default=0)
	watchers	=	models.ManyToManyField(User, blank=True)
	
	def __unicode__(self):
		return u"%s" % (self.name)
	
	class Meta:
        	verbose_name_plural = "Companies"
        	
class Position(models.Model):
	company		=	models.ForeignKey("Company")
	name		=	models.CharField(max_length=32, blank=True)
	description	=	models.TextField(blank=True)
	
	job_domain	=	models.IntegerField(choices=JOB_DOMAIN)
	training_provided=	models.BooleanField(default=True)
	schedule_type	=	models.IntegerField(choices=SCHEDULE_TYPE)
	hiring_method	=	models.IntegerField(choices=HIRING_METHOD)	
	
	hard_mins	=	models.ForeignKey(Mins, related_name="hard", blank=True, null=True)
	pref_mins	=	models.ForeignKey(Mins, related_name="pref", blank=True, null=True)
	
	hiring_direct	=	models.ManyToManyField("Base", related_name="direct", blank=True)
	hiring_possible	=	models.ManyToManyField("Base", related_name="possible", blank=True)
	
	def __unicode__(self):
		return u"%s %s" % (self.company.name, self.name)
		
class Operation(models.Model):
	company		=	models.ForeignKey("Company")
	fleet		=	models.ManyToManyField("Fleet", blank=True, null=True)
	bases		=	models.ManyToManyField("Base", through="OpBase", blank=True)
	positions	=	models.ManyToManyField("Position", blank=True)
	
	def __unicode__(self):
		airplane = []
		for fleet in self.fleet.all():
			airplane.append(fleet.aircraft.type)
	
		return u"%s - %s" % (self.company, ", ".join(airplane))

class OpBase(models.Model):
	operation	=	models.ForeignKey("Operation")
	base		=	models.ForeignKey("Base")
	
	workforce_size	=	models.IntegerField(default=1)	
	routes		=	models.ManyToManyField("Route", related_name="route_opbase", blank=True)
	
	def routes_json(self):
		output = []
		for route in self.routes.all():
			output.append(route.js_lines())
		return "[" + ",".join(output) + "]"
	
	def __unicode__(self):	
		return u"%s - %s" % (self.base.identifier, self.operation.company.name)

		
######################################################################################################


