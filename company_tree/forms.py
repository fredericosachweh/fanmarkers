from django import forms
from django.forms import ModelForm
from django.forms.forms import BoundField
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from models import *
#from constants import *
from airport.models import Airport

############################################################################

class PositionForm(ModelForm):
	class Meta:
		model = Position
		exclude = ('watchers','hard_mins', 'pref_mins', 'company', 'advertising')

class CompanyForm(ModelForm):
	class Meta:
		model = Company
		exclude = ('watchers',)
		
class FleetForm(ModelForm):
	class Meta:
		model = Fleet
		exclude = ('watchers', 'company')
		
class OperationForm(ModelForm):
	positions = forms.ModelMultipleChoiceField(
			queryset=Position.objects.all(),
			widget=forms.CheckboxSelectMultiple,
		)
	
	fleet = forms.ModelMultipleChoiceField(
			queryset=Fleet.objects.all(),
			widget=forms.CheckboxSelectMultiple,
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
			
class OpBaseForm(ModelForm):

	base = forms.ModelChoiceField(queryset=Airport.objects.all(), widget=forms.TextInput)
	
	class Meta:
		model = OpBase
		extra = 0
		
OpBaseFormset = inlineformset_factory(Operation, OpBase, form=OpBaseForm, extra=3, )		

############################################################################
			
class StatusForm(ModelForm):
	not_bases =    forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
	choice_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
	assign_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
	layoff_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)

	class Meta:
		model = Status

##############################################################################
##############################################################################
		
class CompanySearch(forms.Form):
	search		=	forms.CharField(max_length=100, required=False)
	type		=	forms.ChoiceField(choices=[(-1,"Any",),]+BUSINESS_TYPE, label="Business Type")
	jumpseat	=	forms.ChoiceField(choices=[(-1,"Any",),]+JUMPSEAT_TYPE)






