from django.db import models
from django.db.models import Q, permalink
from django.contrib.auth.models import User

from constants import *
from mins import Mins, MinsCatClass, MinsOnType

from aircraft.models import Aircraft
from airport.models import Airport

from django.template.defaultfilters import slugify

#from comment.models import Comment

###############################################################################################################################

class PayscaleYear(models.Model):
    compensation    =       models.ForeignKey("Compensation", )
    year            =       models.IntegerField()
    amount          =       models.FloatField()
    salary_unit     =       models.IntegerField(choices=SALARY_TYPE)

    def __unicode__(self):
        return u"%s (%s)" % (self.compensation.position, self.year)

###############################################################################################################################

class Compensation(models.Model):
    position        =       models.ForeignKey("Position", )

    benefits        =       models.TextField(blank=True)
    perdiem         =       models.TextField("Per Diem", blank=True)

    training_pay    =       models.IntegerField(choices=PAY_TYPE, default=0)
    training_contract=      models.BooleanField(default=False)

    extra_info      =       models.TextField(blank=True)
    last_modified   =       models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "comp: %s" % self.position

###############################################################################################################################

class Fleet(models.Model):
    company         =       models.ForeignKey("Company", )
    aircraft        =       models.ForeignKey(Aircraft)
    size            =       models.IntegerField("Fleet Size", default=1)
    description     =       models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % (self.aircraft, )

    @permalink
    def get_edit_url(self):
        return ('edit-fleet', [str(self.pk)] )

###############################################################################################################################

class Company(models.Model):
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

    @permalink
    def get_absolute_url(self):
        return ('view-company', [str(self.pk), self.slug] )

    @permalink
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

###############################################################################################################################

class Position(models.Model):
    company         =       models.ForeignKey("Company", )
    name            =       models.CharField("Position Name", max_length=32,)
    description     =       models.TextField(blank=True)

    job_domain      =       models.IntegerField(choices=JOB_DOMAIN, default=0)
    schedule_type   =       models.IntegerField(choices=SCHEDULE_TYPE, default=0)

    mins            =       models.ForeignKey(Mins, blank=True, null=True)

    last_modified   =       models.DateTimeField(auto_now=True)
    watchers        =       models.ManyToManyField(User, blank=True, )

    class Meta:
        ordering = ["job_domain"]               #so captain shows up first when displayed on the page

    @permalink
    def get_absolute_url(self):
        return ('view-position', [str(self.pk)] )

    @permalink
    def get_edit_url(self):
        return ('edit-position', [str(self.pk)] )

    @permalink
    def get_edit_mins_url(self):
        return ('edit-mins', [str(self.pk)] )

    def fleets(self):
        try:
            fleet = Fleet.objects.filter(operation__positions=self)
        except:
            fleet = None

        return fleet

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
###############################################################################################################################

class Operation(models.Model):
    company         =       models.ForeignKey("Company",)
    fleet           =       models.ManyToManyField("Fleet", blank=True, null=True)
    bases           =       models.ManyToManyField(Airport, through="OpBase", blank=True)
    positions       =       models.ManyToManyField("Position", blank=True)
    flight_hours    =       models.FloatField("Typical Flight Hours", help_text="(per month)", blank=True, null=True)
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
            ret.append(unicode(fleet.aircraft))

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
    operation       =       models.ForeignKey("Operation", )
    base            =       models.ForeignKey(Airport)
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

class HiringManager(models.Manager):
    def get_query_set(self):
        return super(HiringManager, self).get_query_set().filter( Q(assign_bases__isnull=False) | Q(choice_bases__isnull=False) ).distinct()

class NotHiringManager(models.Manager):
    def get_query_set(self):
        return super(HiringManager, self).get_query_set().filter( Q(assign_bases__isnull=True) & Q(choice_bases__isnull=True) ).distinct()


class Status(models.Model):

    position        =       models.ForeignKey("Position")

    reference       =       models.TextField(blank=True, null=True)
    last_modified   =       models.DateTimeField(auto_now=True)

    assign_bases    =       models.ManyToManyField(OpBase, related_name="assign", blank=True)
    choice_bases    =       models.ManyToManyField(OpBase, related_name="choice", blank=True)
    layoff_bases    =       models.ManyToManyField(OpBase, related_name="layoff", blank=True)

    advertising     =       models.BooleanField(default=False)
    ad_start        =       models.DateTimeField(blank=True, null=True)
    ad_stop         =       models.DateTimeField(blank=True, null=True)

    objects         =       models.Manager()
    hiring          =       HiringManager()
    not_hiring      =       NotHiringManager()

    def __unicode__(self):
        return str(self.position) + " - " + str(self.last_modified)
