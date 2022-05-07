from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    ServiceGroup,
)

from users.models import User


# ############ Service Group form validation logic ############
def service_group_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('service_group') is None:
        form.add_error(
            'service_group',
            'A name for the Service Group must be entered.'
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
        service_group_form_validation(self, CreateServiceGroupForm)
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
        service_group_form_validation(self, UpdateServiceGroupForm)
        return self.cleaned_data
