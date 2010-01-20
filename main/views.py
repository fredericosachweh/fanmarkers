# coding: UTF-8

from annoying.decorators import render_to
from company.models import Company
from position.models import Position

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

def remove_uploads(request):
    from django.http import HttpResponse
    return HttpResponse('nothign here', mimetype="text/plain")
