from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from django.forms import ModelForm
from models import *
from position.models import Position
from fleet.models import Fleet
from airport.models import Airport

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

class AirportFinderField(forms.ModelMultipleChoiceField):
    widget = forms.TextInput
    
    def clean(self, value):
        airport = None
        try:
            airport = Airport.objects.get(identifier__iexact=value)
        except:
            airport = Airport.objects.get(identifier__iexact="k" + value)
            
        return airport


class OpBaseForm(ModelForm):

    base = AirportFinderField(queryset=Airport.objects.all())

    class Meta:
        model = OpBase
        extra = 0

OpBaseFormset = inlineformset_factory(Operation,
                                      OpBase,
                                      form=OpBaseForm,
                                      extra=7)

