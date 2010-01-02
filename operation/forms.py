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

###############################################################################

class AirportWidget(forms.TextInput):
    def _format_value_out(self, pk):
        try:
            airport = Airport.objects.get(pk=pk).identifier
        except:
            airport = ""
            
        return airport

    def render(self, name, value, attrs=None):
        value = self._format_value_out(value)
        return super(AirportWidget, self).render(name, value, attrs)
        
    def _has_changed(self, initial, data):
        return super(AirportWidget, self)\
                ._has_changed(self._format_value_out(initial), data)



class AirportFinderField(forms.ModelMultipleChoiceField):
    widget = AirportWidget
    
    def clean(self, value):
        airport = Airport.goon(identifier__iexact=value)
        
        if not airport:
            airport = Airport.goon(identifier__iexact="k" + value)
            
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

