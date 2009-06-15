from django.forms import ModelForm
from django import forms
from models import *
from django.template import Context, loader
from django.forms.forms import BoundField

class TemplatedForm(forms.Form):
	def output_via_template(self):
		"Helper function for fieldsting fields data from form."
		bound_fields = [BoundField(self, field, name) for name, field \
			in self.fields.items()]
		c = Context(dict(form = self, bound_fields = bound_fields))
		t = loader.get_template('mins.html')
		return t.render(c)

	def __str__(self):
		return self.output_via_template()

############################################################################


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		exclude = ('watchers',)
		
class OpBaseForm(ModelForm):

	base = forms.ModelChoiceField(queryset=Base.objects.all(), widget=forms.TextInput)
	
	class Meta:
		model = OpBase
		exclude = ['routes', ]
		extra = 0
		
class PositionForm(ModelForm):
	class Meta:
		model = Position
		exclude = ('watchers','hard_mins', 'pref_mins', 'company')
		
class FleetForm(ModelForm):
	class Meta:
		model = Fleet
		exclude = ('watchers', 'company')
		
class RouteForm(ModelForm):
	class Meta:
		model = Route
		exclude = ('opbase', )
		
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
			
class HiringStatusForm(ModelForm):

	hiring_bases = forms.ModelMultipleChoiceField(
			queryset=Base.objects.all(),
			widget=forms.SelectMultiple,
		)
		
	firing_bases = forms.ModelMultipleChoiceField(
			queryset=Base.objects.all(),
			widget=forms.SelectMultiple,
		)
	
	class Meta:
		model = HiringStatus
		exclude = ('position', 'date', 'advertising')
	
	def __init__(self, *args, **kwargs):
		if kwargs.has_key('bases_queryset'):
			hqs = kwargs['bases_queryset']
			del kwargs['bases_queryset']

		super(HiringStatusForm, self).__init__(*args, **kwargs)
		
		self.fields['hiring_bases'].queryset = hqs
		self.fields['firing_bases'].queryset = hqs
	
class CatClassMinsForm(ModelForm):
	class Meta:
		model = CatClassMins
		#exclude = ('company',)
		
class MinsForm(ModelForm):
	class Meta:
		model = Mins
		exclude = ('any_mins','airplane_mins', 'se_mins', 'me_mins', 'sea_mins', 'mes_mins', 'sim_mins', 'heli_mins', 'glider_mins')
