from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.create_update import update_object, create_object

from annoying.decorators import render_to

from forms import OpBaseFormset, OperationForm
from models import Company, Operation

@login_required()
@render_to('new-edit_operation.html')		
def edit(request, pk):

	operation = get_object_or_404(Operation, pk=pk)
	type="edit"

	if request.method == "POST":
		form    = OperationForm(request.POST, instance=operation)
		formset = OpBaseFormset(request.POST, instance=operation)

		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
	
			return HttpResponseRedirect( operation.company.get_edit_url() )
	else:
		form    = OperationForm(instance=operation)
		formset = OpBaseFormset(instance=operation)


	return locals()
	
@login_required()
@render_to('new-edit_operation.html')       
def new(request, pk):

	company = get_object_or_404(Company, pk=pk)
	type="new"

	if request.method == "POST":
		op = Operation(company=company)
		
		form = OperationForm(request.POST, instance=op)
		
		if form.is_valid():
			op = form.save()
			if op.pk:
				formset = OpBaseFormset(request.POST, instance=op)
				if formset.is_valid():
					
					formset.save()

					return HttpResponseRedirect( company.get_edit_url() )
	else:
		form = OperationForm(instance=Operation(company=company))
		formset = OpBaseFormset()

	return locals()
