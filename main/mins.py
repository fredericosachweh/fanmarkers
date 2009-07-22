from django.db import models
from constants import *

from aircraft.models import Aircraft

def merge(*input):
    return reduce(list.__add__, input, list())

class MinsOnType(models.Model):
    mins            =       models.ForeignKey("Mins")
    aircraft_type   =       models.ForeignKey(Aircraft, verbose_name="Aircraft")

    total           =       models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)
    p_total         =       models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)

    pic             =       models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)
    p_pic           =       models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)

    type_rating     =       models.IntegerField(MINIMUMS_VERBOSE["type_rating"], choices=TYPE_RATING, default=0)
    p_type_rating   =       models.IntegerField(MINIMUMS_VERBOSE["type_rating"], choices=TYPE_RATING, default=0)

    def _hard(self):
        out = [] 
        for title,value in ((MINIMUMS_VERBOSE["total"], self.total), (MINIMUMS_VERBOSE["pic"], self.pic), ):
            if value > 0:
                out.append( (title,value) )

        if self.type_rating > 0:
            out.append(  (MINIMUMS_VERBOSE['type_rating'], self.get_type_rating_display(), ) )

        return out

    def _pref(self):
        out = []

        for title,value in ((MINIMUMS_VERBOSE["total"], self.p_total), (MINIMUMS_VERBOSE["pic"], self.p_pic), ):
            if value > 0:
                out.append( (title,value) )

        if self.p_type_rating > 0:
            out.append( (MINIMUMS_VERBOSE['type_rating'], self.get_p_type_rating_display(), ) )

        return out

#################################################################################################################

class MinsCatClass(models.Model):
    mins            =       models.ForeignKey("Mins")
    category        =       models.IntegerField("Category", choices=MINS_TYPE)

    total           =       models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)
    p_total         =       models.IntegerField(MINIMUMS_VERBOSE["total"], null=True, blank=True)

    pic             =       models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)
    p_pic           =       models.IntegerField(MINIMUMS_VERBOSE["pic"], null=True, blank=True)

    night           =       models.IntegerField(MINIMUMS_VERBOSE["night"], null=True, blank=True)
    p_night         =       models.IntegerField(MINIMUMS_VERBOSE["night"], null=True, blank=True)

    dual_given      =       models.IntegerField(MINIMUMS_VERBOSE["dual_given"], null=True, blank=True)
    p_dual_given    =       models.IntegerField(MINIMUMS_VERBOSE["dual_given"], null=True, blank=True)

    xc              =       models.IntegerField(MINIMUMS_VERBOSE["xc"], null=True, blank=True)
    p_xc            =       models.IntegerField(MINIMUMS_VERBOSE["xc"], null=True, blank=True)

    cert_level      =       models.IntegerField(MINIMUMS_VERBOSE["cert_level"], choices=CERT_LEVEL, default=0)
    p_cert_level    =       models.IntegerField(MINIMUMS_VERBOSE["cert_level"], choices=CERT_LEVEL, default=0)

    instructor      =       models.BooleanField(MINIMUMS_VERBOSE["instructor"], default=False)
    p_instructor    =       models.BooleanField(MINIMUMS_VERBOSE["instructor"], default=False)

    atp_mins        =       models.BooleanField(MINIMUMS_VERBOSE["atp_mins"], default=False)
    p_atp_mins      =       models.BooleanField(MINIMUMS_VERBOSE["atp_mins"], default=False)

    def _hard(self):
        out = []

        if self.cert_level > 0:
            out.append( (MINIMUMS_VERBOSE["cert_level"], self.get_cert_level_display(),) )

        tuple = ((MINIMUMS_VERBOSE["total"],          self.total),
                 (MINIMUMS_VERBOSE["pic"],            self.pic),
                 (MINIMUMS_VERBOSE["night"],          self.night),
                 (MINIMUMS_VERBOSE["dual_given"],     self.dual_given),
                 (MINIMUMS_VERBOSE["xc"],             self.xc),
                 (MINIMUMS_VERBOSE["instructor"],     self.instructor),
                 (MINIMUMS_VERBOSE["atp_mins"],       self.atp_mins),
                )

        for title,value in tuple:
                if value > 0:
                    out.append( (title,value) )

        return out 

    def _pref(self):
        out = []

        if self.p_cert_level > 0:
                out.append( (MINIMUMS_VERBOSE["cert_level"], self.get_p_cert_level_display(),) )

        tuple = ((MINIMUMS_VERBOSE["total"],          self.p_total),
                 (MINIMUMS_VERBOSE["pic"],            self.p_pic),
                 (MINIMUMS_VERBOSE["night"],          self.p_night),
                 (MINIMUMS_VERBOSE["dual_given"],     self.p_dual_given),
                 (MINIMUMS_VERBOSE["xc"],             self.p_xc),
                 (MINIMUMS_VERBOSE["instructor"],     self.p_instructor),
                 (MINIMUMS_VERBOSE["atp_mins"],       self.p_atp_mins),
                )

        for title,value in tuple:
            if value > 0:
                out.append( (title,value) )

        return out 

#################################################################################################################

class Mins(models.Model):

    degree          =       models.IntegerField(MINIMUMS_VERBOSE["degree"], choices=DEGREE, default=0)
    p_degree        =       models.IntegerField(MINIMUMS_VERBOSE["degree"], choices=DEGREE, default=0)

    years_exp       =       models.DecimalField(MINIMUMS_VERBOSE["years_exp"], max_digits=4, decimal_places=2, null=True, blank=True)
    p_years_exp     =       models.DecimalField(MINIMUMS_VERBOSE["years_exp"], max_digits=4, decimal_places=2, null=True, blank=True)

    years_company   =       models.DecimalField(MINIMUMS_VERBOSE["years_company"], max_digits=4, decimal_places=2, null=True, blank=True)
    p_years_company =       models.DecimalField(MINIMUMS_VERBOSE["years_company"], max_digits=4, decimal_places=2, null=True, blank=True)

    seniority       =       models.BooleanField(MINIMUMS_VERBOSE["seniority"], default=False)
    p_seniority     =       models.BooleanField(MINIMUMS_VERBOSE["seniority"], default=False)

    rec             =       models.BooleanField(MINIMUMS_VERBOSE["rec"], default=False)
    p_rec           =       models.BooleanField(MINIMUMS_VERBOSE["rec"], default=False)

    mech_cert_level =       models.IntegerField(MINIMUMS_VERBOSE["mech_cert"], choices=MECH_CERT_LEVEL, default=0)
    p_mech_cert_level=      models.IntegerField(MINIMUMS_VERBOSE["mech_cert"], choices=MECH_CERT_LEVEL, default=0)

    part_135        =       models.IntegerField(MINIMUMS_VERBOSE["part_135"], choices=PART_135, default=0)
    p_part_135      =       models.IntegerField(MINIMUMS_VERBOSE["part_135"], choices=PART_135, default=0)

    extra_info      =       models.TextField(blank=True)

    last_modified   =       models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Minimums"

    def has(self):
        return bool(self._pref() or self._hard())       #returns true if there are any non-zero minimums

    def _pref_general(self):
        out = []

        tuple = (
                 (MINIMUMS_VERBOSE["years_exp"],      self.p_years_exp),
                 (MINIMUMS_VERBOSE["years_company"],  self.p_years_company),
                 (MINIMUMS_VERBOSE["mech_cert"],      self.get_p_mech_cert_level_display()),
                 (MINIMUMS_VERBOSE["rec"],            self.p_rec),
                 (MINIMUMS_VERBOSE["seniority"],      self.p_seniority),
                )
        
        for title,value in tuple:
            if value > 0 and str(value) != "False" and str(value) != "None":
                out.append( (title,value) )

        if self.p_part_135 > 0:
            out.append( ("Part 135 " + self.get_p_part_135_display() + " Minimums", "True", ) )

        if self.p_degree > 0:
            out.append( (MINIMUMS_VERBOSE["degree"], self.get_p_degree_display(),) )

        return out


    def _hard_general(self):
        out = []

        tuple = (
                 (MINIMUMS_VERBOSE["years_exp"],      self.years_exp),
                 (MINIMUMS_VERBOSE["years_company"],  self.years_company),
                 (MINIMUMS_VERBOSE["mech_cert"],      self.get_mech_cert_level_display()),
                 (MINIMUMS_VERBOSE["rec"],            self.rec),
                 (MINIMUMS_VERBOSE["seniority"],      self.seniority),
                )
        
        for title,value in tuple:
            if value > 0 and str(value) != "False" and str(value) != "None":
                out.append( (title,value) )

        if self.part_135 > 0:
            out.append( ("Part 135 " + self.get_part_135_display() + " Minimums", "True", ) )

        if self.degree > 0:
            out.append( (MINIMUMS_VERBOSE["degree"], self.get_degree_display(),) )

        return out


    def _hard(self):
        out = {}

        hard_general = self._hard_general()

        if hard_general:
            out["General"] = hard_general

        for catclass in self.minscatclass_set.all():
            cc = catclass._hard()
            if cc:
                out[catclass.get_category_display()] = cc

        for plane in self.minsontype_set.all():
            pp = plane._hard()
            if pp:
                out[unicode(plane.aircraft_type)] = pp

        return out

    def _pref(self):
        out = {}

        pref_general = self._pref_general()

        if pref_general:
            out["General"] = pref_general

        for catclass in self.minscatclass_set.all():
            cc = catclass._pref()
            if cc:
                out[catclass.get_category_display()] = cc

        for plane in self.minsontype_set.all():
            pp = plane._pref()
            if pp:
                out[unicode(plane.aircraft_type)] = pp

        return out

    def as_table(self):
        pref = self._pref()
        hard = self._hard()

        row = []
        rows = []
        data = ""

        for cat in list(set(hard.keys() + pref.keys())):          # each min category, eg: "Fixed Wing"
        # cat = cat[0]
            if hard.get(cat, None) or pref.get(cat, None):
                heading = "<th>" + cat + ":</th>"

                if hard.get(cat, None):
                    data += "<table class='hard_mins'><tr><th colspan='2'>Essential</th></tr>"

                    for min_item in hard[cat]:              # each hard item, such as Total and cert level
                        title = min_item[0]
                        value = str(min_item[1])
                        if value == "True":
                            data += "<tr><td colspan='2'>" + title + "</td></tr>"
                        else:
                            data += "<tr><td>" + title + ":</td><td>" + value + "</td></tr>"

                    data += "</table>"

                if pref.get(cat, None):
                    data += "<table class='pref_mins'><tr><th colspan='2'>Preferred</th></tr>"

                    for min_item in pref[cat]:              # each pref item, such as Total and cert level
                        title = min_item[0]
                        value = str(min_item[1])
                        if value == "True":
                            data += "<tr><td colspan='2'>" + title + "</td></tr>"
                        else:
                            data += "<tr><td>" + title + "</td><td>" + value + "</td></tr>"


                    data += "</table>"

                rows.append("<tr>" + heading + "<td>" + data + "</td>" + "</tr>")
                data = ""

        return "\n".join(rows)
#################################################################################################################
