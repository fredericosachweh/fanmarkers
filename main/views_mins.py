from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from models import *
from forms import *

##########################################################################################################

#@login_required()
@render_to('edit_mins.html')
def edit(request, pk):

    position = get_object_or_404(Position, pk=pk)

    #############################

    mins = position.mins
    new=False
    if not mins:
        mins = Mins()
        new = True

    #assert False

    #############################

    if request.POST:
        mf = MinsForm(request.POST, instance=mins)
        cat_class_formset = MinsCatClassFormset(request.POST, instance=position, prefix="cat_class")
        on_type_formset = MinsOnTypeFormset(request.POST, instance=position, prefix="on_type")

        if mf.is_valid() and cat_class_formset.is_valid() and on_type_formset.is_valid():

            cat_class_formset.save()
            on_type_formset.save()
            mf.save()

            if new:
                position.mins = mins
                position.save()

            return HttpResponseRedirect( position.get_absolute_url() )


    else:
        mf = MinsForm(instance=mins)
        cat_class_formset = MinsCatClassFormset(instance=position, prefix="cat_class")
        on_type_formset = MinsOnTypeFormset(instance=position, prefix="on_type")

    return locals()
