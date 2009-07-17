from django.db import models
from django.db.models import permalink
from airport.models import Airport
from main.models import OpBase

class Route(models.Model):
	bases		= models.ManyToManyField(Airport, through="RouteBase", blank=True)
	description	= models.TextField(blank=True)
	home		= models.ForeignKey(OpBase, blank=True)
	
	@permalink
	def get_edit_url(self):
		return ('edit-route', str(self.pk) )
	
	def __unicode__(self):
		ret = []
		for rb in self.real_route():
			ret.append(rb.base.identifier)
			
		return "-".join(ret)
		
	def real_route(self):
		
		base = RouteBase(base=self.home.base)		#create a routebase of the home base, so the output is all routebases
		
		points = RouteBase.objects.filter(route__pk=self.pk)
	
		return [base] + list(points) + [base]
		
		
###############################################################################################################################

class RouteBase(models.Model):
	base		= models.ForeignKey(Airport)
	route		= models.ForeignKey("Route")
	sequence	= models.IntegerField(blank=True)
	
	class Meta:
		ordering = ['sequence']

	def __unicode__(self):
		return u"%s" % (self.base,)
