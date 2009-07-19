from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django import forms
from django.forms.util import flatatt, ErrorDict, ErrorList, ValidationError
from django.forms.formsets import DELETION_FIELD_NAME

class DeleteIfEmptyModelForm(ModelForm):
    """
    A ModelForm which marks itself valid and empty if all visible fields are
    blank or all-whitespace.
    """
    def full_clean(self):
        self._errors = ErrorDict()      #added
        if not self.is_bound:
            return
        if not self.is_empty():
            return super(DeleteIfEmptyModelForm, self).full_clean()

    def is_empty(self):
        self.cleaned_data = {}
        if not hasattr(self, '_empty'):
            self._empty = True
            for boundfield in self:
                field = self.fields[boundfield.name]
                value = field.widget.value_from_datadict(
                    self.data, self.files, self.add_prefix(boundfield.name))
                if not boundfield.is_hidden and boundfield.name != DELETION_FIELD_NAME and value is not None and unicode(value).strip(): #changed
                    self._empty = False
                    break
                try:
                    clean_value = field.clean(value)
                except ValidationError:
                    clean_value = ''
                self.cleaned_data[boundfield.name] = clean_value
        return self._empty

class DeleteIfEmptyInlineFormSet(BaseInlineFormSet):
    """
    Modified version of django.forms.models.BaseInlineFormSet for allowing
    deleting objects by emptying their visible fields instead of checking the
    delete checkbox.

    Not overriding _get_deleted_forms() since it doesn't seem to be used in my
    use case.
    """
    def save_existing_objects(self, commit=True):
        self.changed_objects = []
        self.deleted_objects = []
        if not self.get_queryset():
            return []

        saved_instances = []
        for form in self.initial_forms:
            pk_name = self._pk_field.name
            raw_pk_value = form._raw_value(pk_name)

            # clean() for different types of PK fields can sometimes return
            # the model instance, and sometimes the PK. Handle either.
            pk_value = form.fields[pk_name].clean(raw_pk_value)
            pk_value = getattr(pk_value, 'pk', pk_value)

            obj = self._existing_object(pk_value)
            # the change is on this line:
            if self.can_delete and (form.cleaned_data[DELETION_FIELD_NAME] or form.is_empty()):
                raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
                should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
                if should_delete:
                    self.deleted_objects.append(obj)
                    obj.delete()
                    continue
            if form.has_changed():
                self.changed_objects.append((obj, form.changed_data))
                saved_instances.append(self.save_existing(form, obj, commit=commit))
                if not commit:
                    self.saved_forms.append(form)
        return saved_instances

    def add_fields(self, form, index):
        """Override delete field and make it hidden."""
        super(DeleteIfEmptyInlineFormSet, self).add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()
