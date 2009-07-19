from django import forms
from django.forms import ModelForm

from models import Aircraft
from constants import ENGINE_TYPE, CAT_CLASSES

class AircraftForm(ModelForm):
    class Meta:
        model = Aircraft
        exclude = ('watchers', )

class AircraftSearch(forms.Form):
    search          =       forms.CharField(max_length=100, required=False)
    engine_type     =       forms.ChoiceField(choices=[(-1,"Any",),]+ENGINE_TYPE, label="Engine Type", required=False)
    cat_class       =       forms.ChoiceField(choices=[(-1,"Any",),]+CAT_CLASSES, label="Category/Class", required=False)
