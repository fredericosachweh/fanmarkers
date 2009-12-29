from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from django.forms import ModelForm
from models import *


class StatusForm(ModelForm):
    not_bases =    forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
    choice_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
    assign_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)
    layoff_bases = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), widget=forms.HiddenInput, required=False)

    class Meta:
        model = Status

class PayscaleForm(ModelForm):
    class Meta:
        model = PayscaleYear


class CompensationForm(ModelForm):
    class Meta:
        model = Compensation
        exclude = ('position',)

PayscaleFormset = inlineformset_factory(Compensation, PayscaleYear, form=PayscaleForm, extra=5, )
