from django.forms import ModelMultipleChoiceField, HiddenInput, ModelForm

from models import *
from airport.models import Airport

class StatusForm(ModelForm):
    not_bases =    ModelMultipleChoiceField(
                            queryset=Airport.objects.all(),
                            widget=HiddenInput,
                            required=False)
                            
    choice_bases = ModelMultipleChoiceField(
                            queryset=Airport.objects.all(),
                            widget=HiddenInput,
                            required=False)
                            
    assign_bases = ModelMultipleChoiceField(
                            queryset=Airport.objects.all(),
                            widget=HiddenInput,
                            required=False)
                           
    layoff_bases = ModelMultipleChoiceField(
                            queryset=Airport.objects.all(),
                            widget=HiddenInput,
                            required=False)

    class Meta:
        model = Status

class PositionForm(ModelForm):
    class Meta:
        model = Position
        exclude = ('watchers', 'mins', 'company')
