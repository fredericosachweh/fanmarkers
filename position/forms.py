from django.forms import ModelForm
from models import *

class PositionForm(ModelForm):
    class Meta:
        model = Position
        exclude = ('watchers', 'mins', 'company')
