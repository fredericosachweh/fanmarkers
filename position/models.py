from django.db import models
from constants import *
from mins.models import Mins
from main.mixins import GoonMixin

class Position(models.Model, GoonMixin):
    company         =       models.ForeignKey("company.Company")
    name            =       models.CharField("Position Name", max_length=32,)
    description     =       models.TextField(blank=True)

    job_domain      =       models.IntegerField(choices=JOB_DOMAIN, default=0)
    schedule_type   =       models.IntegerField(choices=SCHEDULE_TYPE, default=0)

    mins            =       models.ForeignKey(Mins, blank=True, null=True)

    last_modified   =       models.DateTimeField(auto_now=True)
    watchers        =       models.ManyToManyField('auth.User', blank=True, )

    class Meta:
        ordering = ["job_domain"]               #so captain shows up first when displayed on the page

    @models.permalink
    def get_absolute_url(self):
        return ('view-position', [str(self.pk)] )

    @models.permalink
    def get_edit_url(self):
        return ('edit-position', [str(self.pk)] )

    @models.permalink
    def get_edit_mins_url(self):
        return ('edit-mins', [str(self.pk)] )

    def fleets(self):
        from fleet.models import Fleet
        try:
            fleet = Fleet.objects.filter(operation__positions=self).distinct()
        except Fleet.DoesNotExist:
            fleet = None

        return fleet
        
    def status_since(self):
        try:
            status = self.status_set.all()[0]       #try to get the status object if one exists
        except:
            return ""
            
        return status.last_modified

    def status(self):
        try:
            status = self.status_set.all()[0]       #try to get the status object if one exists
        except:
            return ""

        if status.choice_bases.count() + status.assign_bases.count() > 0:
            return "<span class='position_hiring_alert'>Hiring!</span>"
        else:
            return ""

    def __unicode__(self):
        return u"%s" % (self.name,)

    def opbases(self):
        try:
            return self.operation_set.all()[0].opbase_set.all()
        except:
            return None

    def modified_seconds_ago(self):
        import datetime
        delta = datetime.datetime.now() - self.last_modified
        days = delta.days
        secs = delta.seconds
        return (days * 86400) + secs
        
    def status_modified_seconds_ago(self):
        import datetime
        try:
            delta = datetime.datetime.now() - self.status_set.all()[0].last_modified
        except:
            return 0
            
        days = delta.days
        secs = delta.seconds
        return (days * 86400) + secs

###############################################################################

class HiringManager(models.Manager):
    def get_query_set(self):
        return super(HiringManager, self).get_query_set()\
                                         .filter(
                                            Q(assign_bases__isnull=False)
                                          | Q(choice_bases__isnull=False))\
                                         .distinct()

class NotHiringManager(models.Manager):
    def get_query_set(self):
        return super(HiringManager, self).get_query_set()\
                                         .filter(
                                            Q(assign_bases__isnull=True)
                                          & Q(choice_bases__isnull=True))\
                                         .distinct()


class Status(models.Model, GoonMixin):

    position        =       models.ForeignKey('position.Position')

    reference       =       models.TextField(blank=True, null=True)
    last_modified   =       models.DateTimeField(auto_now=True)

    assign_bases    =       models.ManyToManyField('operation.OpBase',
                                                   related_name="assign",
                                                   blank=True)
                                                   
    choice_bases    =       models.ManyToManyField('operation.OpBase',
                                                   related_name="choice",
                                                   blank=True)
                                                   
    layoff_bases    =       models.ManyToManyField('operation.OpBase',
                                                   related_name="layoff",
                                                   blank=True)
    

    advertising     =       models.BooleanField(default=False)
    ad_start        =       models.DateTimeField(blank=True, null=True)
    ad_stop         =       models.DateTimeField(blank=True, null=True)

    objects         =       models.Manager()
    hiring          =       HiringManager()
    not_hiring      =       NotHiringManager()

    def __unicode__(self):
        return "%s - %s" % (self.position, self.last_modified)
