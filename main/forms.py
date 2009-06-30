from django import forms
from django.forms import ModelForm
from django.forms.forms import BoundField
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from models import *
from django.template import Context, loader


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
		
class FleetForm(ModelForm):
	class Meta:
		model = Fleet
		exclude = ('watchers', 'company')
		
#####################################################################################################
		
class RouteBaseForm(ModelForm):
	base = forms.ModelChoiceField(queryset=Base.objects.all(), widget=forms.TextInput)

	class Meta:
		model = RouteBase
		#exclude = ('sequence', )
		
class RouteForm(ModelForm):
	class Meta:
		model = Route
		exclude = ('opbase', 'bases')
		
RouteBaseFormset = inlineformset_factory(Route, RouteBase, form=RouteBaseForm, extra=5, )
	
#####################################################################################################
		
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

	base = forms.ModelChoiceField(queryset=Base.objects.all(), widget=forms.TextInput)
	
	class Meta:
		model = OpBase
		extra = 0
		
OpBaseFormset = inlineformset_factory(Operation, OpBase, form=OpBaseForm, extra=5, )		

#####################################################################################################

			
class StatusForm(ModelForm):
	not_bases =    forms.ModelMultipleChoiceField(queryset=Base.objects.all(), widget=forms.HiddenInput, required=False)
	choice_bases = forms.ModelMultipleChoiceField(queryset=Base.objects.all(), widget=forms.HiddenInput, required=False)
	assign_bases = forms.ModelMultipleChoiceField(queryset=Base.objects.all(), widget=forms.HiddenInput, required=False)
	layoff_bases = forms.ModelMultipleChoiceField(queryset=Base.objects.all(), widget=forms.HiddenInput, required=False)

	class Meta:
		model = Status

class newBase(object):
	not_checked = ""
	assign_checked = ""
	choice_checked = ""
	layoff_checked = ""
	unknown_checked = ""
	
	identifier = ""
	location_summary = ""
	
	def __unicode__(self):
		return self.identifier
		
class PositionForm(ModelForm):
	class Meta:
		model = Position
		exclude = ('watchers','hard_mins', 'pref_mins', 'company', 'advertising')
		
class PayscaleForm(ModelForm):
	class Meta:
		model = PayscaleYear
		
		
class CompensationForm(ModelForm):
	class Meta:
		model = Compensation
		exclude = ('position',)
		
PayscaleFormset = inlineformset_factory(Compensation, PayscaleYear, form=PayscaleForm, extra=5, )	
		
#####################################################################################################
	
class CatClassMinsForm(ModelForm):
	class Meta:
		model = CatClassMins
		#exclude = ('company',)
		
class MinsForm(ModelForm):
	class Meta:
		model = Mins
		exclude = ('any_mins','airplane_mins', 'se_mins', 'me_mins', 'sea_mins', 'mes_mins', 'sim_mins', 'heli_mins', 'glider_mins')
		
######################################

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = ('user', )
		
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', )
		
#####################################

