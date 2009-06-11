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
	
	cert_level	=	models.IntegerField("Certificate Level", choices=CERT_LEVEL, default=0)
	
	jet		=	models.IntegerField(default=0)
	turbine		=	models.IntegerField(default=0)
	
	instructor	=	models.BooleanField(default=False)
	instrument_instructor=	models.BooleanField(default=False)
	
class Mins(models.Model):
	airplane_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="airplane")	
	
	SEL_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="sel")
	MEL_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="mel")
	SES_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="ses")
	MES_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="mes")
	
	heli_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="heli")
	glider_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="glider")
	any_mins	=	models.ForeignKey("CatClassMins", blank=True, null=True, related_name="any")
	
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
		return "mins"
		
	def instructor_certs(self):
		instructor = []		
				
		for field in (	("Airplane", self.air_cfi_cert_level),
				("Helicopter", self.heli_cfi_cert_level),
				("Glider", self.glider_cfi_cert_level),
			):
		
			if field[1] > 0:
				instructor.append((field[0], INSTRUCTOR_CERT_LEVEL[field[1]][1]))
				
		return instructor
				
				
	def bools(self):
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
		
	def times(self):
		time = []
	
		for field in (	("Total", self.total),
				("Night", self.night),
				("Istrument", self.instrument),
				("PIC", self.pic),
				("Dual Given", self.dual_given),
				("Cross Country", self.xc),
				
				("Jet", self.jet),
				("Helicopter", self.heli),
				("Seaplane", self.ses),
				("Multi-seaplane", self.mes),
				("Turbine", self.turbine),
				("Multi-engine", self.multi),
				("On Type", self.on_type),
				
				("Multi-PIC", self.m_pic),
				("Helicopter-PIC", self.h_pic),
				("Multi-Seaplane PIC", self.s_pic),
				("Seaplane PIC", self.mes_pic),
				("Turbine-PIC", self.t_pic),
				("Jet-PIC", self.jet_pic),
				("Multi-Turbine-PIC", self.mt_pic),
				
				("Years with company", self.years_company),
				("Years of experience", self.years_exp),
			     ):
			
			if field[1] > 0:
				time.append((str(field[1]), field[0]))
				
		return time
		
	def certs(self):
		certs = []
		
		for field in (	("SEL", self.SEL_cert_level),
				("MEL", self.MEL_cert_level),
				("SES", self.SES_cert_level),
				("MES", self.MES_cert_level),
				("Helicopter", self.heli_cert_level),
				("Glider", self.glider_cert_level),
			):
		
			if field[1] > 0:
				certs.append((field[0], CERT_LEVEL[field[1]][1]))
				
		if self.degree:
			certs.append((DEGREE[self.degree][1],))
			
		if self.cert_agency > 0:
			certs.append((CERT_AGENCY[self.cert_agency][1],))	
			
				
		return certs
		
	def display_hard(self):
		return merge(self.certs(), self.times(), self.instructor_certs(), self.bools())
			
	def display_pref(self):
		return merge(self.certs(), self.times(), self.instructor_certs(), self.bools())
		
		
		
		
		
		
		
		
		
		
		
