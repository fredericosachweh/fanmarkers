from django.forms import ModelForm
from django import forms
from models import *


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		exclude = ('watchers',)
		
class OpBaseForm(ModelForm):
	base = forms.CharField()
		
	class Meta:
		model = OpBase
		exclude = ['operation', 'routes']
		extra = 0
		
class PositionForm(ModelForm):
	class Meta:
		model = Position
		exclude = ('watchers','company')
		
class FleetForm(ModelForm):
	class Meta:
		model = Fleet
		exclude = ('watchers', 'company')
		
class OperationForm(ModelForm):
	positions = forms.ModelMultipleChoiceField(
			queryset=Position.objects.all(),
			widget=forms.SelectMultiple,
		)
	
	fleet = forms.ModelMultipleChoiceField(
			queryset=Fleet.objects.all(),
			widget=forms.SelectMultiple,
		)

	class Meta:
		model = Operation
		exclude = ('bases','company')
		
	def __init__(self, *args, **kwargs):
		super(OperationForm, self).__init__(*args, **kwargs)
		if kwargs.has_key('instance'):
			op = kwargs['instance']
			pos = Position.objects.filter(company=op.company.pk)
			fleet = Fleet.objects.filter(company=op.company.pk)
			self.fields['fleet'].queryset = fleet
			self.fields['positions'].queryset = pos
		
		

