from django.forms import ModelForm

from models import Fleet

class FleetForm(ModelForm):
    class Meta:
        model = Fleet
        exclude = ('watchers', 'company')
