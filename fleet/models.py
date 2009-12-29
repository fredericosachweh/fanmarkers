from django.db import models

from company.models import Company
from aircraft.models import Aircraft

class Fleet(models.Model):
    company         =       models.ForeignKey(Company)
    aircraft        =       models.ForeignKey(Aircraft)
    size            =       models.IntegerField("Fleet Size", default=1)
    description     =       models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % (self.aircraft, )

    @models.permalink
    def get_edit_url(self):
        return ('edit-fleet', [str(self.pk)] )
