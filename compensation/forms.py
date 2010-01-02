from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from django.forms import ModelForm
from models import *

class PayscaleForm(ModelForm):
    class Meta:
        model = PayscaleYear

class CompensationForm(ModelForm):
    class Meta:
        model = Compensation
        exclude = ('position',)

PayscaleFormset = inlineformset_factory(Compensation,
                                        PayscaleYear,
                                        form=PayscaleForm,
                                        extra=5,
                                       )
