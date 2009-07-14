from django.db import models
from constants import *
from company_tree.models import Position

def merge(*input):
	return reduce(list.__add__, input, list())
	
class MinsOnType(models.Model):
	position	=	models.ForeignKey(Position)
	aircraft_type	=	models.ForeignKey("aircraft.Aircraft", verbose_name="Aircraft", null=True, blank=True)	
	
	total		=	models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)
	p_total		=	models.IntegerField(MINIMUMS_VERBOSE["total"] + " Preferred", null=True, blank=True)
	
	pic		=	models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)
	p_pic		=	models.IntegerField(MINIMUMS_VERBOSE["pic"] + " Preferred", null=True, blank=True)
	
	type_rating	=	models.IntegerField(MINIMUMS_VERBOSE["type_rating"], choices=TYPE_RATING, default=0)
	p_type_rating	=	models.IntegerField(MINIMUMS_VERBOSE["type_rating"] + " Preferred", choices=TYPE_RATING, default=0)
	
	class Meta:
		verbose_name_plural = "On Type Minimums"
    
class MinsCatClass(models.Model):
	position	=	models.ForeignKey(Position)	
	category	=	models.IntegerField("Category", choices=MINS_TYPE)	
	
	total		=	models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)
	p_total		=	models.IntegerField(MINIMUMS_VERBOSE["total"] + " Preferred", null=True, blank=True)
	
	pic		=	models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)
	p_pic		=	models.IntegerField(MINIMUMS_VERBOSE["pic"] + " Preferred", null=True, blank=True)
	
	night		=	models.IntegerField(MINIMUMS_VERBOSE["night"], null=True, blank=True)
	p_night		=	models.IntegerField(MINIMUMS_VERBOSE["night"] + " Preferred", null=True, blank=True)
	
	inst		=	models.IntegerField(MINIMUMS_VERBOSE["inst"], null=True, blank=True)
	p_inst		=	models.IntegerField(MINIMUMS_VERBOSE["inst"] + " Preferred", null=True, blank=True)
	
	dual_given	=	models.IntegerField(MINIMUMS_VERBOSE["dual_given"], null=True, blank=True)
	p_dual_given	=	models.IntegerField(MINIMUMS_VERBOSE["dual_given"] + " Preferred", null=True, blank=True)
	
	xc		=	models.IntegerField(MINIMUMS_VERBOSE["xc"], null=True, blank=True)
	p_xc		=	models.IntegerField(MINIMUMS_VERBOSE["xc"] + " Preferred", null=True, blank=True)
	
	cert_level	=	models.IntegerField(MINIMUMS_VERBOSE["cert_level"], choices=CERT_LEVEL, default=0)
	p_cert_level	=	models.IntegerField(MINIMUMS_VERBOSE["cert_level"] + " Preferred", choices=CERT_LEVEL, default=0)
	
	endorsed	=	models.BooleanField(MINIMUMS_VERBOSE["endorsed"], default=False)
	p_endorsed	=	models.BooleanField(MINIMUMS_VERBOSE["endorsed"] + " Preferred", default=False)
	
	instructor	=	models.BooleanField(MINIMUMS_VERBOSE["instructor"], default=False)
	p_instructor	=	models.BooleanField(MINIMUMS_VERBOSE["instructor"] + " Preferred", default=False)
	
	atp_mins	=	models.BooleanField(MINIMUMS_VERBOSE["atp_mins"], default=False)
	p_atp_mins	=	models.BooleanField(MINIMUMS_VERBOSE["atp_mins"] + " Preferred", default=False)
	
	inst_rating	=	models.BooleanField(MINIMUMS_VERBOSE["inst_rating"], default=False)
	p_inst_rating	=	models.BooleanField(MINIMUMS_VERBOSE["inst_rating"] + " Preferred", default=False)
	
	class Meta:
		verbose_name_plural = "Category/Class Minimums"
	
	#def __unicode__(self):
		#ret = []
		#for item in self.time_array:
		#	ret.append(item[0] + ": " + item[1])
		#return "min" + ", ".join(ret)
	
	def _time_array(self):
		time = []
		
		for field in (	(MINIMUMS_VERBOSE["total"],		self.total),
				(MINIMUMS_VERBOSE["night"],		self.night),
				(MINIMUMS_VERBOSE["instrument"],	self.instrument),
				(MINIMUMS_VERBOSE["dual_given"],	self.dual_given),
				(MINIMUMS_VERBOSE["xc"],		self.xc),
				(MINIMUMS_VERBOSE["pic"],		self.pic),
				(MINIMUMS_VERBOSE["t_pic"],		self.t_pic),
				(MINIMUMS_VERBOSE["jet_pic"],		self.jet_pic),
				(MINIMUMS_VERBOSE["cert_level"],	self.get_cert_level_display()),
				(MINIMUMS_VERBOSE["jet"],		self.jet),
				(MINIMUMS_VERBOSE["turbine"],		self.turbine),):

			if field[1] > 0 and not field[1] == "None":
				time.append(    (   field[0]  ,    str(field[1])   )          )
				
		for field in (	(MINIMUMS_VERBOSE["instructor"],		self.instructor),
				(MINIMUMS_VERBOSE["instrument_instructor"],	self.instrument_instructor),
				(MINIMUMS_VERBOSE["atp_mins"],			self.atp_mins), ):
				
			if field[1]:
				time.append(    (   field[0], )      )
				
		return time
		
	time_array = property(_time_array)
	
class MinsGen(models.Model):
	position	=	models.ForeignKey(Position)
	degree		=	models.IntegerField(MINIMUMS_VERBOSE["degree"], choices=DEGREE, default=0)
	p_degree	=	models.IntegerField(MINIMUMS_VERBOSE["degree"] + " Preferred", choices=DEGREE, default=0)
	
	years_exp	=	models.DecimalField(MINIMUMS_VERBOSE["years_exp"], max_digits=4, decimal_places=2, null=True, blank=True)
	p_years_exp	=	models.DecimalField(MINIMUMS_VERBOSE["years_exp"] + " Preferred", max_digits=4, decimal_places=2, null=True, blank=True)
	
	years_company	=	models.DecimalField(MINIMUMS_VERBOSE["years_company"], max_digits=4, decimal_places=2, null=True, blank=True)
	p_years_company	=	models.DecimalField(MINIMUMS_VERBOSE["years_company"] + " Preferred", max_digits=4, decimal_places=2, null=True, blank=True)
	
	seniority	=	models.BooleanField(MINIMUMS_VERBOSE["seniority"], default=False)
	p_seniority	=	models.BooleanField(MINIMUMS_VERBOSE["seniority"] + " Preferred", default=False)
	
	rec		=	models.BooleanField(MINIMUMS_VERBOSE["rec"], default=False)
	p_rec		=	models.BooleanField(MINIMUMS_VERBOSE["rec"] + " Preferred", default=False)
	
	mech_cert_level	=	models.IntegerField(MINIMUMS_VERBOSE["mech_cert"], choices=MECH_CERT_LEVEL, default=0)
	p_mech_cert_level=	models.IntegerField(MINIMUMS_VERBOSE["mech_cert"] + " Preferred", choices=MECH_CERT_LEVEL, default=0)
	
	part_135	=	models.IntegerField(MINIMUMS_VERBOSE["part_135"], choices=PART_135, default=0)
	p_part_135	=	models.IntegerField(MINIMUMS_VERBOSE["part_135"] + " Preferred", choices=PART_135, default=0)
	
	inst_instructor=	models.BooleanField(MINIMUMS_VERBOSE["inst_instructor"], default=False)
	p_inst_instructor=	models.BooleanField(MINIMUMS_VERBOSE["inst_instructor"] + " Preferred", default=False)
	
	extra_info	=	models.TextField(blank=True)
	
	last_modified	=	models.DateTimeField(auto_now=True)
	
	#############################################################
	
	class Meta:
        	verbose_name_plural = "General Minimums"
			
	#def __unicode__(self):
	#	pass
		#ret = []
		#for item in self.times:
		#	ret.append( item[1] + " - " + item[0] )
		#return "mins: " + ", ".join(ret)
		
	def _general(self):
		
		gen = []
		
		if self.type_rating:
			gen.append((MINIMUMS_VERBOSE["type_rating"], self.type_rating.type, ))
		
		if self.on_type > 0:
			gen.append((MINIMUMS_VERBOSE["on_type"], self.on_type, ))
		
		if self.years_exp > 0:
			gen.append((MINIMUMS_VERBOSE["years_exp"], self.years_exp, ))	
		
		if self.years_company > 0:
			gen.append((MINIMUMS_VERBOSE["years_company"], self.years_company, ))	
		
		if self.cert_agency > 0:
			gen.append((MINIMUMS_VERBOSE["cert_agency"], self.get_cert_agency_display(), ))
		
		if self.mech_cert_level > 0:
			gen.append((MINIMUMS_VERBOSE["mech_cert"], self.get_mech_cert_level_display(), ))
			
		if self.degree > 0:
			gen.append((MINIMUMS_VERBOSE["degree"], self.get_degree_display(), ))
			
		if self.i135_mins:
			gen.append((MINIMUMS_VERBOSE["i135"],))
			
		if self.v135_mins and not self.i135_mins:			#vfr mins are subset of ifr mins, so ignore vfr when ifr is selected
			gen.append((MINIMUMS_VERBOSE["v135"],))
			
		if self.tailwheel:
			gen.append((MINIMUMS_VERBOSE["tailwheel"],))
			
		if self.seniority:
			gen.append((MINIMUMS_VERBOSE["seniority"],))
			
		if self.rec:
			gen.append((MINIMUMS_VERBOSE["rec"],))

		ret = {}
		
		try:					#don't create a key if the list is empty
			gen[0]
			ret["General"] = gen
			return ret
		except:
			return {}
		
		
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
		
		general.update(times)
		
		all_reqs = general
		
		table = ""
		
		for cat_class in all_reqs:
			title = cat_class
			req_array = all_reqs[cat_class]
			req_string = ""					
			
			for item in req_array:
				try:
					req = str(item[0]) + ": "
					value = "<strong>" + str(item[1]) + "</strong>"
				except:
					req = "<strong>" + str(item[0]) + "</strong>"
					value = ""
					
				req_string = req_string + "<li>" + req + value + "</li> "	
				
			req_string = "<ul>" + req_string + "</ul>"
	
			table = table + title + ":" + req_string

		return  table  #str(times) + "<br/> " + str(general)
	
		
	times = property(_times)
	general = property(_general)
	
	def has(self):
		return self.times.__len__() > 0 or self.general.__len__() > 0
		
	def as_table(self):
		times = self.times
		general = self.general
		
		general.update(times)
		
		all_reqs = general
		
		table = ""
		
		for cat_class in all_reqs:
			title = cat_class
			req_array = all_reqs[cat_class]
			req_string = ""					
			
			for item in req_array:
				try:
					req = str(item[0]) + ": "
					value = "<strong>" + str(item[1]) + "</strong>"
				except:
					req = "<strong>" + str(item[0]) + "</strong>"
					value = ""
					
				req_string = req_string + "<li>" + req + value + "</li>"	
				
			req_string = "<td><ul>" + req_string + "</ul></td>"
	
			table = table + "<tr><th>" + title + ":</th>" + req_string + "</tr>"

		return  table  #str(times) + "<br/> " + str(general)
			
#################################################################################################################

		
		
