from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import *

class MinsCatClassForm(ModelForm):
    class Meta:
        model = MinsCatClass
        exclude = ('mins', 'id', )

class MinsOnTypeForm(ModelForm):
    class Meta:
        model = MinsOnType
        exclude = ('mins', 'id', )

class MinsForm(ModelForm):
    class Meta:
        model = Mins

MinsCatClassFormset = inlineformset_factory(Mins, MinsCatClass, form=MinsCatClassForm, extra=3, exclude=['mins', 'id'])
MinsOnTypeFormset  = inlineformset_factory(Mins, MinsOnType, form=MinsOnTypeForm, extra=1, exclude=['mins', 'id'])

