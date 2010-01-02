from django.db import models
from django.db.models import Q, permalink
from django.contrib.auth.models import User

from main.mixins import GoonMixin
from constants import *

class Operation(models.Model, GoonMixin):
    company         =       models.ForeignKey('company.Company',)
    
    fleet           =       models.ManyToManyField('fleet.Fleet',
                                                   blank=True,
                                                   null=True)
                                                   
    bases           =       models.ManyToManyField('airport.Airport', 
                                                   through="OpBase",
                                                   blank=True)
                                                   
    positions       =       models.ManyToManyField('position.Position',
                                                   blank=True)
                                                   
    flight_hours    =       models.FloatField("Typical Flight Hours",
                                              help_text="(per month)",
                                              blank=True,
                                              null=True)
                                              
    extra_info      =       models.TextField("Extra Info", blank=True)
    last_modified   =       models.DateTimeField(auto_now=True)

    @permalink
    def get_edit_url(self):
        return ('edit-operation', [str(self.pk)] )

    def __unicode__(self):
        return u"%s - %s" % (self.company, self.all_fleet)

    def _all_fleet(self):
        ret = []
        for fleet in self.fleet.all():
            ret.append(unicode(fleet.aircraft.type))

        return " + ".join(ret)

    def _all_bases(self):
        ret = []
        for base in self.bases.all():
            ret.append(unicode(base.identifier))

        return ", ".join(ret)

    all_bases = property(_all_bases)
    all_fleet = property(_all_fleet)



###############################################################################################################################

class OpBase(models.Model):
    operation       =       models.ForeignKey(Operation)
    base            =       models.ForeignKey('airport.Airport')
    info            =       models.TextField("Extra Info", blank=True)

    hiring_status   =       "not"
    verbose_hiring_status=  HIRING_STATUS["not"]

    def __unicode__(self):
        return u"%s - %s" % (self.base.identifier, self.operation.company.name)

    def routes_json(self):
        output = []
        for route in self.route_set.all():
            output.append(route.json())
        return "[" + ",".join(output) + "]"

    def fill_in_status(self, status):
        assign_bases = status.assign_bases.all()
        choice_bases = status.choice_bases.all()
        layoff_bases = status.layoff_bases.all()

        if self in assign_bases:
            self.hiring_status = "assign"
            self.verbose_hiring_status = HIRING_STATUS["assign"]

        elif self in choice_bases:
            self.hiring_status = "choice"
            self.verbose_hiring_status = HIRING_STATUS["choice"]

        elif self in layoff_bases:
            self.hiring_status = "layoff"
            self.verbose_hiring_status = HIRING_STATUS["layoff"]
        else:
            self.hiring_status = "not"
            self.verbose_hiring_status = HIRING_STATUS["not"]


###############################################################################################################################


