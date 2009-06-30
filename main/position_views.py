from django.contrib.auth.decorators import login_required
from main.models import *

from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

########################################################################

@login_required()
@render_to('new_position.html')	
def new_position(request, pk):
	from forms import PositionForm

	company = get_object_or_404(Company, pk=pk)

	if request.method == "POST":
		pos = Position(company=company)
		form = PositionForm(request.POST, instance=pos)
	
		if form.is_valid():
			form.save(commit=False)
			form.hard_mins = Mins()
			form.pref_mins = Mins()
			form.save()
			return HttpResponseRedirect( "/edit" + company.get_absolute_url() )
	else:
		form = PositionForm()
	
	return {'company': company, 'form': form}
	
########################################################################
	
#@login_required()
@render_to('edit_position.html')		
def edit_position(request, pk):
	from forms import StatusForm, PositionForm, CompensationForm, PayscaleFormset
	
	position = get_object_or_404(Position, pk=pk)
	operation = get_object_or_None(Operation, positions=position)
	
	if operation:
		opbases = operation.opbase_set.all()
		bases = Base.objects.filter(opbase__in=opbases)
	else:
		bases = []
		opbases = []
	
	#######################################################################
	
	status = get_object_or_None(Status, position=position)
	if not status:
		status = Status(position=position)
		
	compensation = get_object_or_None(Compensation, position=position)
	if not compensation:
		compensation = Compensation(position=position)
		
	pref_mins = position.pref_mins
	if not pref_mins:
		pref_mins = Mins()
		
	hard_mins = position.hard_mins
	if not hard_mins:
		hard_mins = Mins()
		
	#assert False
	
	#######################################################################
		
	if request.method == "POST":
		
		newPOST = request.POST.copy()
		newPOST.update({"position": position.pk})
		
		field_bases = rearrange_fields(newPOST, bases)	
					
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
			#	payscale_formset.save()
			#######
		
			instance = status_form.save(commit=False)
			
			if list(instance.not_bases.all()) != field_bases["not"] or \
			list(instance.not_bases.all()) != field_bases["layoff"] or \
			list(instance.assign_bases.all()) != field_bases["assign"] or \
			list(instance.choice_bases.all()) != field_bases["choice"] and \
			status_form.has_changed():			#only run this block of code of the status has changed otherwise the last modified value will change
				status_form.save()
				c="C"
			
				instance.not_bases = field_bases["not"]
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
		newbases = make_newbases(bases, status)
		
		pos_form = PositionForm(instance=position)
		comp_form = CompensationForm(instance=compensation)
	
	return {"payscale_formset": payscale_formset,
		"comp_form": comp_form,
		"bases": newbases,
		"status_form": status_form,
		"position": position,
		"pos_form": pos_form,
		"last_modified": status.last_modified}

###################################################################	
###################################################################
###################################################################
###################################################################
	
def rearrange_fields(newPOST, bases):
	field_bases = {}
	field_bases["not"] = field_bases["assign"] = field_bases["choice"] = field_bases["layoff"] = []
	
	for base in bases:
		for item in ("not", "assign", "choice", "layoff", ):
			if newPOST[str(base)] == item:
				field_bases[item] = field_bases[item] + [base]
	return field_bases
	
def make_newbases(bases, status):
	from main.forms import newBase
	
	newbases = []
	
	for base in bases:
		
		newbase = newBase()
		newbase.identifier = base.identifier
		newbase.location_summary = base.location_summary
		
		if not status.pk:
			newbase.unknown_checked = 'checked="checked"'
			
		elif base in status.not_bases.all():
			newbase.not_checked = 'checked="checked"'
			
		elif base in status.choice_bases.all():
			newbase.choice_checked = 'checked="checked"'
			
		elif base in status.assign_bases.all():
			newbase.assign_checked = 'checked="checked"'
			
		elif base in status.layoff_bases.all():
			newbase.layoff_checked = 'checked="checked"'
			
		else:
			newbase.unknown_checked = 'checked="checked"'
		
		newbases.append(newbase)
		
	return newbases

	
