from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    ServiceGroup,
    Objective,
)

from users.models import User

from ops.models import (
    PEeP,
    LEE,
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
    if cleaned_data.get('objective_development_template') == '2) Descriptive' and cleaned_data.get('opportunity_statement') is None:
        form.add_error(
            'opportunity_statement',
            'An Opportunity Statement must be entered.'
        )
    elif cleaned_data.get('objective_development_template') == '3) Change' and cleaned_data.get('opportunity_statement') is None:
        form.add_error(
            'opportunity_statement',
            'An Opportunity Statement must be entered.'
        )
    elif cleaned_data.get('objective_development_template') == '2) Descriptive' and cleaned_data.get('objective_statement') is None:
        form.add_error(
            'objective_statement',
            'An Objective Statement must be entered.'
        )
    elif cleaned_data.get('objective_development_template') == '3) Change' and cleaned_data.get('objective_statement') is None:
        form.add_error(
            'objective_statement',
            'An Objective Statement must be entered.'
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


# ####################### Create Objective Form #######################
class CreateObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        fields = [
            'objective',
            'service_group',
            'objective_status',
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


# ####################### Update Objective Form #######################
class UpdateObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        fields = [
            'objective',
            'service_group',
            'objective_status',
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


# ####################### PEeP Create Form #######################
class CreatePEePForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsible'].queryset = User.objects.filter(is_staff=True)
        self.fields['supervisor'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = PEeP

        fields = [
            'process_function',
            'process_code',
            'responsible',
            'display_name',
            'supervisor',
            'whurthy_team',
            'detailed_description',
        ]


# ####################### PEeP Update Form #######################
class UpdatePEePForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsible'].queryset = User.objects.filter(is_staff=True)
        self.fields['supervisor'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = PEeP

        fields = [
            'process_function',
            'process_code',
            'responsible',
            'display_name',
            'supervisor',
            'whurthy_team',
            'detailed_description',
        ]


# ####################### LEE Create Form #######################
class CreateLEEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_owner'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = LEE
        fields = [
            'process_role',
            'whurthy_application',
            'relevant_file',
            'process_description',
            'entry_owner',
            'process_code',
            'process_outcome'
        ]


# ####################### LEE Update Form #######################
class UpdateLEEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_owner'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = LEE
        fields = [
            'process_role',
            'whurthy_application',
            'relevant_file',
            'process_description',
            'entry_owner',
            'process_code',
            'process_outcome'
        ]
