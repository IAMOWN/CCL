from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    ServiceGroup,
    Objective,
)


# ############ Service Group form validation logic ############
def service_group_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('service_group') is None:
        form.add_error(
            'service_group',
            'A name for the Service Group must be entered.'
        )
    return


# ############ Objective form validation logic ############
def objective_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('objective') is None:
        form.add_error(
            'objective',
            'A name for the Objective must be entered.'
        )
    return


# ####################### Create Service Group Form #######################
class CreateServiceGroupForm(forms.ModelForm):

    class Meta:
        model = ServiceGroup
        fields = [
            'service_group',
            'members',
            'purpose',
            'qualified_intentions',
            'service_group_type',
            'service_group_status',
        ]

    def clean(self):
        objective_form_validation(self, CreateServiceGroupForm)
        return self.cleaned_data


# ####################### Update Service Group Form #######################
class UpdateServiceGroupForm(forms.ModelForm):

    class Meta:
        model = ServiceGroup
        fields = [
            'service_group',
            'members',
            'purpose',
            'qualified_intentions',
            'service_group_type',
            'service_group_status',
        ]

    def clean(self):
        objective_form_validation(self, UpdateServiceGroupForm)
        return self.cleaned_data


# ####################### Create Service Group Form #######################
class CreateObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        fields = [
            'objective',
            'service_group',
            'objective_development_template',
            'opportunity_statement',
            'objective_statement',
            'awareness',
            'clarity',
            'emergence',
            'discipline',
        ]

    def clean(self):
        objective_form_validation(self, CreateObjectiveForm)
        return self.cleaned_data


# ####################### Update Service Group Form #######################
class UpdateObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        fields = [
            'objective',
            'service_group',
            'objective_development_template',
            'opportunity_statement',
            'objective_statement',
            'awareness',
            'clarity',
            'emergence',
            'discipline',
        ]

    def clean(self):
        objective_form_validation(self, UpdateObjectiveForm)
        return self.cleaned_data
