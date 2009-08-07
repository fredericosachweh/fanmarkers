# coding: UTF-8

from django.contrib.auth.decorators import login_required
from models import *

from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

#############################################################################################################################

@render_to('list_latest.html')
def latest(request):
    positions = Position.objects.order_by('-last_modified').select_related()[:15]
    companies = Company.objects.order_by('-last_modified')[:15]

    return locals()
    
@render_to('about.html')
def about(request):
    positions = Position.objects.all().count()
    companies = Company.objects.all().count()
    return locals()

















