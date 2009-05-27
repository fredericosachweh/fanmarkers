from django.forms import ModelForm
from django import forms
from models import *


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		exclude = ('watchers',)
		
class OpBaseForm(ModelForm):
	base = forms.CharField()
	route= RouteField()
	
	class Meta:
		model = OpBase
		exclude = ('operation')
