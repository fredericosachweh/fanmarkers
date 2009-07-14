from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, permalink


from constants import *

###############################################################################################################################
	
class Fleet(models.Model):
	company		=	models.ForeignKey("Company", )
	aircraft	=	models.ForeignKey("aircraft.Aircraft")
	size		=	models.IntegerField("Fleet Size", default=1)
	description	=	models.TextField(blank=True)
	
	@permalink
	def get_edit_url(self):
		return ('edit-fleet', str(self.pk) )

	def __unicode__(self):
		return u"%s" % (self.aircraft, )

###############################################################################################################################

class Company(models.Model):
	name		=	models.CharField(max_length=64, unique=True)
	call_sign	=	models.CharField(max_length=32, blank=True)
	website		=	models.URLField(blank=True)
	description	=	models.TextField(blank=True)
	type		=	models.IntegerField(choices=BUSINESS_TYPE, default=0)
	jumpseat	=	models.IntegerField(choices=JUMPSEAT_TYPE, default=0)
	union		=	models.CharField(max_length=32, blank=True, default="")
	contact_info	=	models.TextField(blank=True)
	watchers	=	models.ManyToManyField(User, blank=True, )
	last_modified	=	models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name_plural = "Companies"
		
	@permalink
	def get_absolute_url(self):
		return ('view-company', str(self.pk) )
		
	@permalink
	def get_edit_url(self):
		return ('edit-company', str(self.pk) )

		
	def __unicode__(self):
		return u"%s" % (self.name)
	
###############################################################################################################################

class Operation(models.Model):
	company		=	models.ForeignKey("Company",)
	fleet		=	models.ManyToManyField("Fleet", blank=True, null=True)
	bases		=	models.ManyToManyField("airport.Airport", through="OpBase", blank=True)
	positions	=	models.ManyToManyField("Position", blank=True)
	flight_hours	=	models.FloatField("Typical Flight Hours", help_text="(per month)", blank=True, null=True)
	extra_info	=	models.TextField("Extra Info", blank=True)
	last_modified	=	models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return u"%s - %s" % (self.company, self.all_fleet)
		
	@permalink
	def get_edit_url(self):
		return ('edit-operation', str(self.pk) )
		
	def _all_fleet(self):
		ret = []
		for fleet in self.fleet.all():
			ret.append(unicode(fleet.aircraft))
			
		return " + ".join(ret)
			
	def _all_bases(self):
		ret = []
		for base in self.bases.all():
			ret.append(unicode(base.identifier))
			
		return ", ".join(ret)
		
	all_bases = property(_all_bases)
	all_fleet = property(_all_fleet)
	
	

###############################################################################################################################

class OpBase(models.Model):
	operation	=	models.ForeignKey("Operation", )
	base		=	models.ForeignKey("airport.Airport", )
	info		=	models.TextField("Extra Info", blank=True)
	
	hiring_status	=	"unknown"
	verbose_hiring_status=	HIRING_STATUS["unknown"]
	
	def __unicode__(self):	
		return u"%s - %s" % (self.base.identifier, self.operation.company.name)
		
	def routes_json(self):
		output = []
		for route in self.route_set.all():
			output.append(route.json())
		return "[" + ",".join(output) + "]"
		
	def fill_in_status(self, status):
		not_bases = status.not_bases.all()
		assign_bases = status.assign_bases.all()
		choice_bases = status.choice_bases.all()
		layoff_bases = status.layoff_bases.all()

		if self in not_bases:
			self.hiring_status = "not"
			self.verbose_hiring_status = HIRING_STATUS["not"]
			
		elif self in assign_bases:
			self.hiring_status = "assign"
			self.verbose_hiring_status = HIRING_STATUS["assign"]
		
		elif self in choice_bases:
			self.hiring_status = "choice"
			self.verbose_hiring_status = HIRING_STATUS["choice"]
		
		elif self in layoff_bases:
			self.hiring_status = "layoff"
			self.verbose_hiring_status = HIRING_STATUS["layoff"]
		else:
			self.hiring_status = "unknown"
			self.verbose_hiring_status = HIRING_STATUS["unknown"]
	

###############################################################################################################################

class Position(models.Model):
	company		=	models.ForeignKey("Company", )
	name		=	models.CharField("Position Name", max_length=32, blank=True)
	description	=	models.TextField(blank=True)
	
	job_domain	=	models.IntegerField(choices=JOB_DOMAIN)
	schedule_type	=	models.IntegerField(choices=SCHEDULE_TYPE)

	last_modified	=	models.DateTimeField(auto_now=True)
	watchers	=	models.ManyToManyField(User, blank=True, )
		
	class Meta:	
		ordering = ["job_domain"]		#so captain shows up first when displayed on the page
		
	@permalink
	def get_absolute_url(self):
		return ('view-position', str(self.pk) )
		
	@permalink
	def get_edit_url(self):
		return ('edit-position', str(self.pk) )
		
	def __unicode__(self):
		return u"%s" % (self.name,)

	def opbases(self):
		try:
			return self.operation_set.all()[0].opbase_set.all()
		except:
			return None
			
###############################################################################################################################

class HiringManager(models.Manager):
	def get_query_set(self):
		return super(HiringManager, self).get_query_set().filter( Q(assign_bases__isnull=False) | Q(choice_bases__isnull=False) ).distinct()
		
class NotHiringManager(models.Manager):
	def get_query_set(self):
		return super(HiringManager, self).get_query_set().filter( Q(assign_bases__isnull=True) & Q(choice_bases__isnull=True) ).distinct()		

		
class Status(models.Model):

	position	=	models.ForeignKey("Position")
	
	reference	=	models.TextField(blank=True, null=True)
	last_modified	=	models.DateTimeField(auto_now=True)
	
	not_bases	=	models.ManyToManyField("OpBase", related_name="not", blank=True)
	assign_bases	=	models.ManyToManyField("OpBase", related_name="assign", blank=True)
	choice_bases	=	models.ManyToManyField("OpBase", related_name="choice", blank=True)
	layoff_bases	=	models.ManyToManyField("OpBase", related_name="layoff", blank=True)
	
	advertising	=	models.BooleanField(default=False)
	ad_start	=	models.DateTimeField(blank=True, null=True)
	ad_stop		=	models.DateTimeField(blank=True, null=True)
	
	objects		=	models.Manager()
	hiring		=	HiringManager()
	not_hiring	=	NotHiringManager()
	
	def __unicode__(self):
		return str(self.position) + " - " + str(self.last_modified)
