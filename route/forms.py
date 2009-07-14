from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from empty_formset import DeleteIfEmptyInlineFormSet, DeleteIfEmptyModelForm
from models import *

class RouteBaseForm(DeleteIfEmptyModelForm): ###DeleteIfEmptyModelForm
	base = forms.ModelChoiceField(widget=forms.TextInput)

	class Meta:
		model = RouteBase
		
class RouteForm(ModelForm):
	class Meta:
		model = Route
		exclude = ('opbase', 'bases')
		
RouteBaseFormset = inlineformset_factory(Route, RouteBase, form=RouteBaseForm, formset=DeleteIfEmptyInlineFormSet, extra=5, can_delete=True)
