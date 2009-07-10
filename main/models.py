from django.db import models
from django.contrib.auth.models import User
from constants import *
from mins import Mins, CatClassMins
from base.models import Airport
from django.db.models import Q

###############################################################################################################################

class Aircraft(models.Model):
	manufacturer	=	models.CharField(max_length=32, help_text="e.g: Cessna, Beechcraft")
	type		=	models.CharField(max_length=32, help_text="e.g: C-172, BE-76")
	model		=	models.CharField(max_length=64, help_text="e.g: Skyhawk, Duchess", blank=True)
	extra		=	models.CharField(max_length=32, help_text="e.g: RG, on floats", blank=True)
	engine_type	=	models.IntegerField(choices=ENGINE_TYPE, default=0)
	cat_class	=	models.IntegerField("Category/Class", choices=CAT_CLASSES, default=1)
	watchers	=	models.ManyToManyField(User, blank=True, )
	
	class Meta:	
		ordering = ["manufacturer", "type"]
		
	def get_absolute_url(self):
		return "/aircraft/%i/" % self.pk

		
	def __unicode__(self):
	

		if self.extra:
			model = " " + self.model + " " + self.extra

		elif self.model:
			model = " " + self.model

		else:
			model = ""
			
			
		return u'%s (%s%s)' % (self.type, self.manufacturer, model, )

###############################################################################################################################
		
class PayscaleYear(models.Model):
	compensation	=	models.ForeignKey("Compensation", )
	year		=	models.IntegerField()
	amount		=	models.FloatField()
	salary_unit	=	models.IntegerField(choices=SALARY_TYPE)
	
	def __unicode__(self):
		return u"%s (%s)" % (self.compensation.position, self.year)
		
###############################################################################################################################
		
class Compensation(models.Model):
	position	=	models.ForeignKey("Position", )
	
	benefits	=	models.TextField(blank=True)
	perdiem		=	models.TextField("Per Diem", blank=True)
	
	training_pay	=	models.IntegerField(choices=PAY_TYPE, default=0)
	training_contract=	models.BooleanField(default=False)

	extra_info	=	models.TextField(blank=True)
	last_modified	=	models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return "comp: %s" % self.position
		
###############################################################################################################################
		
class Route(models.Model):
	bases		=	models.ManyToManyField(Airport, through="RouteBase", blank=True)
	description	=	models.TextField(blank=True)
	opbase		=	models.ForeignKey("OpBase", blank=True)
	
	def __unicode__(self):
		ret = []
		for rb in self.real_route():
			ret.append(rb.base.identifier)
			
		return "-".join(ret)
		
	def json(self):
		ret = []
		for base in self.bases.all():
			ret.append('[' + str(base.location.y) + ', ' + str(base.location.x) + ']')
		
		return '[' + ",".join(ret) + ']'
		
	def real_route(self):
		
		base = RouteBase(base=self.opbase.base)
		
		points = RouteBase.objects.filter(route__pk=self.pk)
	
		return [base] + list(points) + [base]
		
		
###############################################################################################################################

class RouteBase(models.Model):
	base		=	models.ForeignKey(Airport)
	route		=	models.ForeignKey("Route")
	sequence	=	models.IntegerField(blank=True)
	
	class Meta:
		ordering = ['sequence']

	def __unicode__(self):
		return u"%s" % (self.base,)
		
###############################################################################################################################		
	
class Fleet(models.Model):
	company		=	models.ForeignKey("Company", )
	aircraft	=	models.ForeignKey("Aircraft")
	size		=	models.IntegerField("Fleet Size", default=1)
	description	=	models.TextField(blank=True)

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
		
	def get_absolute_url(self):
		return "/company/%i/" % self.pk 
		
	def __unicode__(self):
		return u"%s" % (self.name)
	
###############################################################################################################################
        	
class Position(models.Model):
	company		=	models.ForeignKey("Company", )
	name		=	models.CharField("Position Name", max_length=32, blank=True)
	description	=	models.TextField(blank=True)
	
	job_domain	=	models.IntegerField(choices=JOB_DOMAIN)
	schedule_type	=	models.IntegerField(choices=SCHEDULE_TYPE)
	
	hard_mins	=	models.ForeignKey(Mins, related_name="hard", blank=True, null=True)
	pref_mins	=	models.ForeignKey(Mins, related_name="pref", blank=True, null=True)
	last_modified	=	models.DateTimeField(auto_now=True)
	watchers	=	models.ManyToManyField(User, blank=True, )
		
	class Meta:	
		ordering = ["job_domain"]		#so captain shows up first when displayed on the page
		
	def get_absolute_url(self):
		return "/position/%i/" % self.pk
		
	def __unicode__(self):
		return u"%s" % (self.name,)

	def opbases(self):
		try:
			return self.operation_set.all()[0].opbase_set.all()
		except:
			return None

###############################################################################################################################

class Operation(models.Model):
	company		=	models.ForeignKey("Company",)
	fleet		=	models.ManyToManyField("Fleet", blank=True, null=True)
	bases		=	models.ManyToManyField(Airport, through="OpBase", blank=True)
	positions	=	models.ManyToManyField("Position", blank=True)
	flight_hours	=	models.FloatField("Typical Flight Hours", help_text="(per month)", blank=True, null=True)
	extra_info	=	models.TextField("Extra Info", blank=True)
	last_modified	=	models.DateTimeField(auto_now=True)
	
	def get_absolute_url(self):
		return "/company/%s/#op%s" % (self.company.pk, self.pk)
	
	def __unicode__(self):
		return u"%s - %s" % (self.company, self.all_fleet)
		
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
	base		=	models.ForeignKey(Airport)
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
	
	not_bases	=	models.ManyToManyField(OpBase, related_name="not", blank=True)
	assign_bases	=	models.ManyToManyField(OpBase, related_name="assign", blank=True)
	choice_bases	=	models.ManyToManyField(OpBase, related_name="choice", blank=True)
	layoff_bases	=	models.ManyToManyField(OpBase, related_name="layoff", blank=True)
	
	advertising	=	models.BooleanField(default=False)
	ad_start	=	models.DateTimeField(blank=True, null=True)
	ad_stop		=	models.DateTimeField(blank=True, null=True)
	
	objects		=	models.Manager()
	hiring		=	HiringManager()
	not_hiring	=	NotHiringManager()
	
	def __unicode__(self):
		return str(self.position) + " - " + str(self.last_modified)
	
###############################################################################################################################

class Profile(models.Model):
	user		=	models.ForeignKey(User, primary_key=True)
					
	dob		=	models.DateField("Date of Birth", blank=True, default="1900-01-01")
	#resume		=	models.FileField(upload_to="resume/")










