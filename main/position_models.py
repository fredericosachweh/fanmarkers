from django.db import models
from constants import *
from mins import *
from django.contrib import admin

class Position(models.Model):
	company		=	models.ForeignKey("Company")
	name		=	models.CharField(max_length=32, blank=True)
	description	=	models.TextField(blank=True)
	
	job_domain	=	models.IntegerField(choices=JOB_DOMAIN)
	training_provided=	models.BooleanField(default=True)
	schedule_type	=	models.IntegerField(choices=SCHEDULE_TYPE)
	hiring_method	=	models.IntegerField(choices=HIRING_METHOD)
	rec_essential	=	models.BooleanField(default=False)

	salary_amount	=	models.IntegerField(default=0)
	salary_unit	=	models.IntegerField(choices=SALARY_TYPE)
	
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
	
	def routes_center(self):
		all_longs = []
		all_lats = []
		
		for r in self.routes.all():
			lat_long = r.center()
			all_lats.append(lat_long[0])
			all_longs.append(lat_long[1])
			
		if len(all_lats) == 0:
			return "None"
			
		avg_lat = (max(all_lats) + min(all_lats)) / 2
		avg_long = (max(all_longs) + min(all_longs)) / 2
		
		return (avg_lat, avg_long)
		
	def routes_json(self):
		output = []
		for route in self.routes.all():
			output.append(route.js_lines())
		return "[" + ",".join(output) + "]"
	
	def __unicode__(self):	
		return u"%s - %s" % (self.base.identifier, self.operation.company.name)
