from django.forms import ModelForm
from django import forms

from models import *
from constants import *

class AircraftForm(ModelForm):
	class Meta:
		model = Aircraft
		exclude = ('watchers', )
		
class AircraftSearch(forms.Form):
	search		=	forms.CharField(max_length=100, required=False)
	engine_type	=	forms.ChoiceField(choices=[(-1,"Any",),]+ENGINE_TYPE, label="Engine Type")
	cat_class	=	forms.ChoiceField(choices=[(-1,"Any",),]+CAT_CLASSES, label="Category/Class")
