from django.forms import ModelForm
from django import forms

from models import *
from constants import *

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('watchers',)

class FleetForm(ModelForm):
    class Meta:
        model = Fleet
        exclude = ('watchers', 'company')
        

BUSINESS_TYPE_ANY = [(-1,"Any",),] + BUSINESS_TYPE
JUMPSEAT_TYPE_ANY = [(-1,"Any",),] + JUMPSEAT_TYPE

class CompanySearch(forms.Form):
    search =   forms.CharField(max_length=100, required=False)
    type =     forms.ChoiceField(choices=BUSINESS_TYPE_ANY, label="Business Type")
    jumpseat = forms.ChoiceField(choices=JUMPSEAT_TYPE_ANY)
