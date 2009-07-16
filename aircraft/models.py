from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from constants import *

class Aircraft(models.Model):
	manufacturer	=	models.CharField(max_length=32, help_text="e.g: Cessna, Beechcraft")
	type		=	models.CharField(max_length=32, help_text="e.g: C-172, BE-76")
	model		=	models.CharField(max_length=64, help_text="e.g: Skyhawk, Duchess", blank=True)
	extra		=	models.CharField(max_length=32, help_text="e.g: RG, on floats", blank=True)
	engine_type	=	models.IntegerField("Engine Type", choices=ENGINE_TYPE, default=0)
	cat_class	=	models.IntegerField("Category/Class", choices=CAT_CLASSES, default=1)
	watchers	=	models.ManyToManyField(User, blank=True, )
	
	class Meta:	
		ordering = ["manufacturer", "type"]
		
	@permalink
	def get_absolute_url(self):
		return ('view-aircraft', str(self.pk) )
		
	@permalink
	def get_edit_url(self):
		return ('edit-aircraft', str(self.pk) )

		
	def __unicode__(self):
	

		if self.extra:
			model = " " + self.model + " " + self.extra

		elif self.model:
			model = " " + self.model

		else:
			model = ""
			
			
		return u'%s (%s%s)' % (self.type, self.manufacturer, model, )
