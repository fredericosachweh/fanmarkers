from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import *
from forms import *

from compensation.models import *
from compensation.forms import *

########################################################################

@render_to('view_position.html')	
def view(request, pk):
	position = get_object_or_404(Position, pk=pk)
	
	try:
		opbases = position.operation_set.all()[:1].opbase_set.all()
	except AttributeError:
		opbases = []
	
	try:
		fleets = position.operation_set.all()[:1].fleet.all()
	except AttributeError:
		fleets = []
		
	compensation = get_object_or_None(Compensation, position=position)
	if compensation:
		payscales = compensation.payscaleyear_set.all()
		
	
	
	status = get_object_or_None(Status, position=position)
	if status:
		not_bases = status.not_bases.all()
		assign_bases = status.assign_bases.all()
		choice_bases = status.choice_bases.all()
		layoff_bases = status.layoff_bases.all()
		
		for opbase in opbases:
			opbase.fill_in_status(status)
	
	watchers = position.watchers.count()
	
	if request.user in position.watchers.all():
		already_watching = True
	
	
	
		
	return locals()


@login_required()
@render_to('new_position.html')	
def new(request, pk):

	company = get_object_or_404(Company, pk=pk)

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
	
#@login_required()
@render_to('edit_position.html')		
def edit(request, pk):
	
	position = get_object_or_404(Position, pk=pk)
	operation = get_object_or_None(Operation, positions=position)
	
	if operation:
		opbases = operation.opbase_set.all()
	else:
		opbases = []
	
	#######################################################################
	
	status = get_object_or_None(Status, position=position)
	if not status:
		status = Status(position=position)
		
	compensation = get_object_or_None(Compensation, position=position)
	if not compensation:
		compensation = Compensation(position=position)
		
	#######################################################################
		
	if request.method == "POST":
		
		newPOST = request.POST.copy()
		newPOST.update({"position": position.pk})
		
		#assert False
		
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
			
			if list(instance.not_bases.all()) != field_bases["not"] or \
				list(instance.not_bases.all()) != field_bases["layoff"] or \
				list(instance.assign_bases.all()) != field_bases["assign"] or \
				list(instance.choice_bases.all()) != field_bases["choice"] and \
				status_form.has_changed() or not status_form.instance.pk:
				#only if the status has changed or its the first edit, otherwise dont run because we dont want the 'last modified' value to change
				
					status_form.save()
					
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
		mark_opbases(opbases, status)
		
		pos_form = PositionForm(instance=position)
		comp_form = CompensationForm(instance=compensation)
	
	return {"payscale_formset": payscale_formset,
		"comp_form": comp_form,
		"opbases": opbases,
		"status_form": status_form,
		"position": position,
		"pos_form": pos_form,
		"last_modified": status.last_modified}
		
@render_to('list_position.html')
def make_list(request):

	positions = Position.objects.all()
	
	return locals()

###################################################################	
###################################################################
###################################################################
###################################################################
	
def rearrange_fields(newPOST, opbases):
	field_bases = {}
	field_bases["not"] = field_bases["assign"] = field_bases["choice"] = field_bases["layoff"] = []
	
	for opbase in opbases:
		for item in ("not", "assign", "choice", "layoff", ):
			if newPOST["opb-" + str(opbase.pk)] == item:			# if airport exists in approprate column...
				field_bases[item] = field_bases[item] + [opbase]	# add that airport object to the appropriate list
	return field_bases
	
def mark_opbases(opbases, status):

	for opbase in opbases:
		if not status.pk:
			opbase.unknown_checked = 'checked="checked"'
			
		elif opbase in status.not_bases.all():
			opbase.not_checked = 'checked="checked"'
			
		elif opbase in status.choice_bases.all():
			opbase.choice_checked = 'checked="checked"'
			
		elif opbase in status.assign_bases.all():
			opbase.assign_checked = 'checked="checked"'
			
		elif opbase in status.layoff_bases.all():
			opbase.layoff_checked = 'checked="checked"'
			
		else:
			opbase.unknown_checked = 'checked="checked"'

	
