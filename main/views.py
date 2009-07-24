# coding: UTF-8

from django.contrib.auth.decorators import login_required
from models import *

from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

###############################################################################

@login_required()
@render_to('profile.html')
def profile(request):
    from main.forms import ProfileForm, UserForm

    user = request.user
    profile = get_object_or_None(Profile, user=user)

    if not profile:
        profile = Profile(user=user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            return HttpResponseRedirect( "/" )
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)

    return locals()

#############################################################################################################################

@render_to('list_latest.html')
def latest(request):
    positions = Position.objects.order_by('-last_modified').select_related()[:15]
    #aircrafts = Aircraft.objects.order_by('-last_modified')[:15]
    companies = Company.objects.order_by('-last_modified')[:15]

    return locals()
