from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

class GoonMixin(object):
    @classmethod
    def goon(cls, *args, **kwargs):
        return get_object_or_None(cls, *args, **kwargs)
    
    @classmethod
    def goof(cls, *args, **kwargs):
        return get_object_or_404(cls, *args, **kwargs)
