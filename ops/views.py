from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render

from .models import (
    ServiceGroup,
    Objective,
)

from .forms import (
    CreateServiceGroupForm,
    UpdateServiceGroupForm,
    CreateObjectiveForm,
    UpdateObjectiveForm,
)


# FUNCTIONS
def get_current_year():
    return datetime.now().year


# ####################### SERVICE GROUP VIEWS #######################
class ServiceGroupList(LoginRequiredMixin, ListView):
    model = ServiceGroup
    template_name = 'ops/service_groups.html'
    context_object_name = 'service_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'EGA Service Groups'

        return context


# ####################### Service Group - Detail View #######################
class ServiceGroupDetail(LoginRequiredMixin, DetailView):
    model = ServiceGroup
    template_name = 'ops/service_group_detail.html'
    context_object_name = 'service_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"EGA Service Group: {ServiceGroup.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Service Group - Create View #######################
class ServiceGroupCreate(LoginRequiredMixin, CreateView):
    model = ServiceGroup
    form_class = CreateServiceGroupForm
    template_name = 'ops/service_group_form.html'

    def form_valid(self, form):
        message = form.instance.service_group
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Service Group "{message}" has been added'
        )
        return super(ServiceGroupCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Service Group - Update View #######################
class ServiceGroupUpdate(LoginRequiredMixin, UpdateView):
    model = ServiceGroup
    form_class = UpdateServiceGroupForm
    template_name = 'ops/service_group_form.html'

    def form_valid(self, form):
        message = form.instance.service_group
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Service Group "{message}" has been updated'
        )
        return super(ServiceGroupUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Service Group - Delete View #######################
class ServiceGroupDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceGroup
    template_name = 'ops/service_group_confirm_delete.html'
    success_url = reverse_lazy('service-groups')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


# ####################### OBJECTIVE VIEWS #######################
class ObjectiveList(LoginRequiredMixin, ListView):
    model = Objective
    template_name = 'ops/objectives.html'
    context_object_name = 'objectives'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Service Group Objectives'

        return context


# ####################### Objective - Detail View #######################
class ObjectiveDetail(LoginRequiredMixin, DetailView):
    model = Objective
    template_name = 'ops/objective_detail.html'
    context_object_name = 'objective'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Objective: {Objective.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Objective - Create View #######################
class ObjectiveCreate(LoginRequiredMixin, CreateView):
    model = Objective
    form_class = CreateObjectiveForm
    template_name = 'ops/objective_form.html'

    def form_valid(self, form):
        message = form.instance.objective
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Objective "{message}" has been added'
        )
        return super(ObjectiveCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectiveCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Objective - Update View #######################
class ObjectiveUpdate(LoginRequiredMixin, UpdateView):
    model = Objective
    form_class = UpdateObjectiveForm
    template_name = 'ops/objective_form.html'

    def form_valid(self, form):
        message = form.instance.objective
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Objective "{message}" has been updated'
        )
        return super(ObjectiveUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectiveUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Objective - Delete View #######################
class ObjectiveDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Objective
    template_name = 'ops/objective_confirm_delete.html'
    success_url = reverse_lazy('objectives')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectiveDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context

