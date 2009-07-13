from models import *
from main.models import Position
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

class MinsCatClassForm(ModelForm):
	class Meta:
		model = MinsCatClass
		exclude = ('mins', 'id', )
		
class MinsOnTypeForm(ModelForm):
	class Meta:
		model = MinsOnType
		exclude = ('mins', 'id', )
		
class MinsGenForm(ModelForm):
	class Meta:
		model = MinsGen
		
MinsCatClassFormset = inlineformset_factory(Position, MinsCatClass, form=MinsCatClassForm, extra=3, exclude=['mins', 'id'])
MinsOnTypeFormset = inlineformset_factory(Position, MinsOnType, form=MinsOnTypeForm, extra=3, exclude=['mins', 'id'])
