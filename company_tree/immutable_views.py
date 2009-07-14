from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from models import *



@render_to('view_jobmap.html')
def jobmap(request):
	
	usa_bases = OpBase.objects.filter(base__country__exact="US")
	alaska_bases = usa_bases.filter(base__region__name__exact="AK")
	russia_bases = OpBase.objects.filter(base__country__exact="RU")
	india_bases = OpBase.objects.filter(base__country__exact="IN")
	canada_bases = OpBase.objects.filter(base__country__exact="CA")
	
	usa_h = Status.objects.filter(   Q(assign_bases__in=usa_bases) | Q(choice_bases__in=usa_bases)    ).distinct().count()
	usa_t = Position.objects.filter( operation__opbase__in=usa_bases ).distinct().count()

	canada_h = Status.objects.filter(   Q(assign_bases__in=canada_bases) | Q(choice_bases__in=canada_bases)    ).distinct().count()
	canada_t = Position.objects.filter( operation__opbase__in=canada_bases ).distinct().count()
	
	india_h = Status.objects.filter(   Q(assign_bases__in=india_bases) | Q(choice_bases__in=india_bases)    ).distinct().count()
	india_t = Position.objects.filter( operation__opbase__in=india_bases ).distinct().count()

	russia_h = Status.objects.filter(   Q(assign_bases__in=russia_bases) | Q(choice_bases__in=russia_bases)    ).distinct().count()
	russia_t = Position.objects.filter( operation__opbase__in=russia_bases ).distinct().count()
	
	alaska_h = Status.objects.filter(   Q(assign_bases__in=alaska_bases) | Q(choice_bases__in=alaska_bases)    ).distinct().count()
	alaska_t = Position.objects.filter( operation__opbase__in=alaska_bases ).distinct().count()

	return locals()
