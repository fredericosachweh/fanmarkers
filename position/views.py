from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.db.models import Q

from annoying.decorators import render_to

from compensation.models import Compensation
from aircraft.models import Aircraft
from company.models import Company
from operation.models import Operation

from models import *
from forms import *
from constants import *

########################################################################

@render_to('view_position.html')
def view(request, pk):
    position = Position.goof(pk=pk)

    opbases = position.opbases()

    compensation = Compensation.goon(position=position)
    if compensation:
        payscales = compensation.payscaleyear_set.all()

    status = Status.goon(position=position)

    if status:
        assign_bases = status.assign_bases.all()
        choice_bases = status.choice_bases.all()
        layoff_bases = status.layoff_bases.all()

        for opbase in opbases:
            opbase.fill_in_status(status)

    #watchers = position.watchers.count()

    if request.user in position.watchers.all():
        already_watching = True

    kmz_url = reverse("kml-position", kwargs={"pk": position.pk})

    return locals()


@login_required()
@render_to('new_position.html')
def new(request, pk):

    company = Company.goof(pk=pk)

    if request.method == "POST":
        pos = Position(company=company)
        form = PositionForm(request.POST, instance=pos)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(company.get_edit_url() )
    else:
        form = PositionForm()

    return {'company': company, 'form': form}

########################################################################

@login_required()
@render_to('edit_position.html')
def edit(request, pk):
    from compensation.forms import PayscaleFormset, CompensationForm
    
    position = Position.goof(pk=pk)
    operation = Operation.goon(positions=position)

    if operation:
        opbases = operation.opbase_set.all()
    else:
        opbases = []

    #######################################################################

    status = Status.goon(position=position)
    if not status:
        status = Status(position=position)

    compensation = Compensation.goon(position=position)
    if not compensation:
        compensation = Compensation(position=position)

    #######################################################################

    if request.method == "POST":
        
        newPOST = request.POST.copy()
        newPOST.update({"position": position.pk})

        field_bases = rearrange_fields(newPOST, opbases)

        status_form = StatusForm(newPOST, instance=status)
        pos_form = PositionForm(newPOST, instance=position)
        comp_form = CompensationForm(newPOST, instance=compensation)
        payscale_formset = PayscaleFormset(newPOST, instance=compensation)

        if status_form.is_valid() and pos_form.is_valid() and comp_form.is_valid() and payscale_formset.is_valid():
            if pos_form.has_changed():
                pos_form.save()

            if comp_form.has_changed():
                comp_form.save()

            #if payscale_formset.has_changed():
            payscale_formset.save()
            #######

            if not status_form.instance.pk:
                instance = status_form.save()
            else:
                instance = status_form.save(commit=False)

            if      list(instance.layoff_bases.all()) != field_bases["layoff"] or \
                    list(instance.assign_bases.all()) != field_bases["assign"] or \
                    list(instance.choice_bases.all()) != field_bases["choice"] and \
                    status_form.has_changed() or not status_form.instance.pk:
                #only if the status has changed or its the first edit, otherwise dont run because we dont want the 'last modified' value to change

                status_form.save()

                instance.layoff_bases = field_bases["layoff"]
                instance.assign_bases = field_bases["assign"]
                instance.choice_bases = field_bases["choice"]
                instance.save()

            #assert False
            #######

            return HttpResponseRedirect( position.get_absolute_url() )
    else:
        payscale_formset = PayscaleFormset(instance=compensation)

        status_form = StatusForm(instance=status)
        mark_opbases(opbases, status)

        pos_form = PositionForm(instance=position)
        comp_form = CompensationForm(instance=compensation)

    return {"payscale_formset": payscale_formset,
            "comp_form": comp_form,
            "opbases": opbases,
            "status_form": status_form,
            "position": position,
            "operation": operation,
            "pos_form": pos_form,
            "last_modified": status.last_modified}

##################################################################

JOB_DOMAIN_ANY = [(-1, "Any")] + JOB_DOMAIN

class PositionSearch(forms.Form):
    search       = forms.CharField(max_length=100, required=False)
    job_domain   = forms.ChoiceField(choices=JOB_DOMAIN_ANY, required=False)
    aircraft     = forms.ModelChoiceField( queryset=Aircraft.objects.all(), required=False )
    status       = forms.ChoiceField( choices=[(-1, "Any"), (0, "Not Hiring"), (1, "Hiring")], required=False)

##################################################################

@render_to('list_position.html')
def make_list(request):

    positions = Position.objects.all().order_by('name', 'job_domain')
    title = "Positions"

    if request.GET.get("status", False):

        get = request.GET
        searchform = PositionSearch(get)

        domain =   int(get.get("job_domain", -1))
        search =       get.get("search", "")
        aircraft =     get.get("aircraft", "")#when aircraft is left "---", it returns a blank value
        status =   int(get.get("status", -1))

        if domain > 0:
            positions = positions.filter( job_domain=domain )
                
        if search:
            positions = positions.filter( name__icontains=search )

        if aircraft != "":
            positions = positions.filter( operation__fleet__aircraft=aircraft)

        if status == 0:
            positions = (positions
                            .filter(
                                       Q(status__assign_bases__isnull=True)
                                     & Q(status__choice_bases__isnull=True)
                             )
                        )

        if status == 1:
            positions = (positions
                            .filter(
                                       Q(status__assign_bases__isnull=False)
                                     | Q(status__choice_bases__isnull=False)
                             )
                            .distinct()
                        )
    else:
        searchform = PositionSearch()

    return locals()

##############################################################################

def kml(request, pk):
    from route.models import Route
    from airport.models import Airport
    
    position = Position.goof(pk=pk)
    
    routes = Route.objects.filter(home__operation__positions=position)
    
    bases = Airport.objects\
                   .filter(opbase__operation__positions=position)\
                   .distinct()
                   
    routebases = Airport.objects\
                        .filter(routebase__route__in=routes)\
                        .exclude(opbase__operation__positions=position)\
                        .distinct()
                        
    title = "%s - %s" % (position.company, position)

    
    from kml.utils import locals_to_kmz_response
    return locals_to_kmz_response(locals())

###################################################################
###################################################################
###################################################################
###################################################################






def rearrange_fields(newPOST, opbases):
    field_bases = {}
    field_bases["assign"] = field_bases["choice"] = field_bases["layoff"] = []

    for opbase in opbases:
        for item in ("assign", "choice", "layoff", ):
            if newPOST["opb-" + str(opbase.pk)] == item:                    # if airport exists in approprate column...
                field_bases[item] = field_bases[item] + [opbase]        # add that airport object to the appropriate list
    return field_bases

def mark_opbases(opbases, status):

    for opbase in opbases:
        if not status.pk:
            opbase.not_checked = 'checked="checked"'

        elif opbase in status.choice_bases.all():
            opbase.choice_checked = 'checked="checked"'

        elif opbase in status.assign_bases.all():
            opbase.assign_checked = 'checked="checked"'

        elif opbase in status.layoff_bases.all():
            opbase.layoff_checked = 'checked="checked"'

        else:
            opbase.not_checked = 'checked="checked"'
