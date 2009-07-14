from django.db import models

class Route(models.Model):
	bases		=	models.ManyToManyField("airport.Airport", through="RouteBase", blank=True)
	description	=	models.TextField(blank=True)
	start_stop	=	models.ForeignKey("company_tree.OpBase", blank=True)
	
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
	base		=	models.ForeignKey("airport.Airport")
	route		=	models.ForeignKey("Route")
	sequence	=	models.IntegerField(blank=True)
	
	class Meta:
		ordering = ['sequence']

	def __unicode__(self):
		return u"%s" % (self.base,)
