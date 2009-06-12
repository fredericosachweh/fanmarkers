from django.db import models
from constants import *

def merge(*input):
	return reduce(list.__add__, input, list())
    
class CatClassMins(models.Model):
	total		=	models.IntegerField(default=0)
	night		=	models.IntegerField(default=0)
	instrument	=	models.IntegerField(default=0)
	dual_given	=	models.IntegerField("Instruction Given", default=0)
	xc		=	models.IntegerField("Cross Country", default=0)
	
	pic		=	models.IntegerField("PIC", default=0)
	t_pic		=	models.IntegerField("Turbine-PIC", default=0)
	jet_pic		=	models.IntegerField("Jet-PIC", default=0)
	
	jet		=	models.IntegerField(default=0)
	turbine		=	models.IntegerField(default=0)
	
	cert_level	=	models.IntegerField("Certificate Level", choices=CERT_LEVEL, default=0)
	instructor	=	models.BooleanField(default=False)
	instrument_instructor=	models.BooleanField(default=False)
	
	def __unicode__(self):
		
		ret = []
		
		for item in self.time_array:
			ret.append(item[0] + ": " + item[1])
		
		return ", ".join(ret)
	
	def _time_array(self):
		time = []
		
		for field in (	("Total",		self.total),
				("Night",		self.night),
				("Istrument",		self.instrument),
				("Instruction Given",	self.dual_given),
				("Cross Country",	self.xc),
				("PIC",			self.pic),
				("Turbine-PIC",		self.t_pic),
				("Jet-PIC",		self.jet_pic),
				("Certification Level",	self.get_cert_level_display()),
				("Jet",			self.jet),
				("Turbine",		self.turbine),
				("Instructor",		self.instructor),
				("Instrument Instructor",self.instrument_instructor),):

			if field[1] > 0 and not field[1] == "None":
				time.append(    (   str(field[0])    ,    str(field[1])   )          )
				
		return time
		
	time_array = property(_time_array)
	
class Mins(models.Model):

	any_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="any")
	airplane_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="airplane")
	
	se_mins		=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="se")
	me_mins		=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="me")
	sea_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="sea")
	mes_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="mes")
	
	heli_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="heli")
	glider_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="glider")
	
	sim_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="sim")
	
	#############################################################
	
	on_type		=	models.IntegerField("On Type", default=0)

	years_exp	=	models.DecimalField("Years of Experience", max_digits=4, decimal_places=2, default=0)
	years_company	=	models.DecimalField("Years with this Company", max_digits=4, decimal_places=2, default=0)
	
	seniority	=	models.BooleanField(default=False)
	rec		=	models.BooleanField("Internal Recommendation", default=False)
	
	mech_cert_level	=	models.IntegerField("Mechanic", choices=MECH_CERT_LEVEL, default=0)
	
	cert_agency	=	models.IntegerField(choices=CERT_AGENCY, default=0)
	atp_mins	=	models.BooleanField("ATP Minimums", default=False)
	i135_mins	=	models.BooleanField("Part 135 IFR Minimums", default=False)
	v135_mins	=	models.BooleanField("Part 135 VFR Minimums", default=False)
	tailwheel	=	models.BooleanField("Tailwheel Endorsement", default=False)
	
	degree		=	models.IntegerField("Education", choices=DEGREE, default=0)
	
	type_rating	=	models.ForeignKey("Aircraft", null=True, blank=True)
	
	#############################################################
	
	class Meta:
        	verbose_name_plural = "Mins"
			
	def __unicode__(self):
	
		ret = []
		
		for item in self.times:
			ret.append( item[1] + " - " + item[0] )
		
		return ", ".join(ret)
		
	def _general(self):
		spec = []
		
		if self.atp_mins:
			spec.append(("ATP Mins",))
			
		if self.i135_mins:
			spec.append(("Part 135 IFR Minimums",))
			
		if self.v135_mins and not self.i135_mins:			#vfr mins are subset of ifr mins, so ignore vfr when ifr is selected
			spec.append(("Part 135 VFR Minimums",))
			
		if self.tailwheel:
			spec.append(("Tailwheel Endorsement",))
			
		if self.seniority:
			spec.append(("Enough Seniority",))
			
		if self.rec:
			spec.append(("Internal Recommendation",))
			
		return spec
		
	def _times(self):
		time = {}
	
		for cat_class in (
				(self.airplane_mins,"Any Fixed Wing"), 
				(self.any_mins, "Any Aircraft"),
				(self.se_mins, "Single-Engine Airplane"),
				(self.me_mins, "Multi-Engine Airplane"),
				(self.sea_mins, "Single-Engine Seaplane"),
				(self.mes_mins, "Multi-Engine Seaplane"),
				(self.glider_mins, "Glider"),
				(self.heli_mins, "Helicopter"),
				(self.sim_mins, "Simulator"),):
				
			if cat_class[0]:
				time[cat_class[1]] = cat_class[0].time_array
				
		return time
		
	def as_ul(self):
		times = self.times
		general = self.general
		
		table = ""
		
		for cat_class in times:
			title = cat_class
			req_array = times[cat_class]
			req_string = ""					
			
			req_string = req_string + "<ul>"
			for item in req_array:
				req_string = req_string + "<li>" + str(item[0]) + ": <strong>" + str(item[1]) + "</strong></li> "	
			req_string = req_string + "</ul>"
	
			table = table + title + ":" + req_string

		return table
	
		
	times = property(_times)
	general = property(_general)
			
#################################################################################################################

		
		
