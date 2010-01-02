from django.template.defaultfilters import slugify
from django.db import models

from constants import *
from main.mixins import GoonMixin

User = models.get_model('auth','user')
Aircraft = models.get_model('aircraft','aircraft')

class Company(models.Model, GoonMixin):
    name            =       models.CharField(max_length=64, unique=True)
    call_sign       =       models.CharField(max_length=32, blank=True)
    website         =       models.URLField(blank=True)
    description     =       models.TextField(blank=True)
    type            =       models.IntegerField(choices=BUSINESS_TYPE, default=0)
    jumpseat        =       models.IntegerField(choices=JUMPSEAT_TYPE, default=0)
    union           =       models.CharField(max_length=32, blank=True, default="")
    contact_info    =       models.TextField(blank=True)
    watchers        =       models.ManyToManyField(User, blank=True, )
    last_modified   =       models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name',]

    @models.permalink
    def get_absolute_url(self):
        return ('view-company', [str(self.pk), self.slug] )

    @models.permalink
    def get_edit_url(self):
        return ('edit-company', [str(self.pk)] )

    def __unicode__(self):
        return u"%s" % (self.name)

    def slugify(self):
        return slugify(self.name)

    def modified_seconds_ago(self):
        import datetime
        delta = datetime.datetime.now() - self.last_modified
        days = delta.days
        secs = delta.seconds
        return ( days * 86400 ) + secs


    slug = property(slugify)
