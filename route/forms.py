from django.forms import ModelForm
from empty_formset import DeleteIfEmptyInlineFormSet, DeleteIfEmptyModelForm
from django.forms.models import inlineformset_factory
from django import forms

from models import Route, RouteBase
from airport.models import *

class RouteBaseForm(DeleteIfEmptyModelForm):
    base = forms.ModelChoiceField(queryset=Airport.objects.all(), widget=forms.TextInput)

    class Meta:
        model = RouteBase

class RouteForm(ModelForm):
    class Meta:
        model = Route
        exclude = ('home', 'bases')

RouteBaseFormset = inlineformset_factory(Route, RouteBase, form=RouteBaseForm, formset=DeleteIfEmptyInlineFormSet, extra=5, can_delete=True)
