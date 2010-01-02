from annoying.functions import get_object_or_None

class GoonMixin(object):
    @classmethod
    def goon(cls, *args, **kwargs):
        return get_object_or_None(cls, *args, **kwargs)
