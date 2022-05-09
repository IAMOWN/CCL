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
    LEE,
    PEeP,
)

from .forms import (
    CreateServiceGroupForm,
    UpdateServiceGroupForm,
    CreateObjectiveForm,
    UpdateObjectiveForm,
    CreateLEEForm,
    UpdateLEEForm,
    CreatePEePForm,
    UpdatePEePForm,
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

        service_group = ServiceGroup.objects.get(id=self.kwargs['pk'])
        context['objectives'] = Objective.objects.filter(service_group=service_group)

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


# ####################### Objective for Service Group - Create View #######################
class ObjectiveServiceGroupCreate(LoginRequiredMixin, CreateView):
    model = Objective
    form_class = CreateObjectiveForm
    template_name = 'ops/objective_for_service_group_form.html'

    def form_valid(self, form):
        service_group = ServiceGroup.objects.get(id=self.kwargs['pk'])
        form.instance.service_group = service_group
        form.save()

        message = form.instance.objective
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Objective "{message}" has been added'
        )
        return super(ObjectiveServiceGroupCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectiveServiceGroupCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()
        context['service_group'] = ServiceGroup.objects.get(id=self.kwargs['pk'])

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


# ####################### LEE #######################
class LEEListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """LEE ListView."""
    model = LEE
    template_name = 'ops/support_lee.html'
    context_object_name = 'LEE'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()

        context['search_off'] = True
        search_input = self.request.GET.get('search-area') or ''
        code_search_input = self.request.GET.get('code-search-area') or ''
        owner_search_input = self.request.GET.get('owner-search-area') or ''
        if search_input:
            context['LEE'] = context['LEE'].filter(process_role__icontains=search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = search_input
            context['search_type'] = 'Role'
            context['search_off'] = False
        if code_search_input:
            context['LEE'] = context['LEE'].filter(whurthy_application__icontains=code_search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = code_search_input
            context['search_type'] = 'App'
            context['search_off'] = False
        if owner_search_input:
            context['LEE'] = context['LEE'].filter(entry_owner__username__icontains=owner_search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = owner_search_input
            context['search_type'] = 'Owner'
            context['search_off'] = False

        context['search_input'] = search_input

        return context


class LEEDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """LEE DetailView."""
    model = LEE
    template_name = 'ops/support_lee_detail.html'
    context_object_name = 'LEE'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(LEEDetailView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


class LEECreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """LEE CreateView."""
    model = LEE
    form_class = CreateLEEForm

    template_name = 'ops/support_lee_form.html'

    success_url = reverse_lazy('support-lee')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        message = form.instance.process_role
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The LEE entry "{message}" has been added.'
        )
        return super(LEECreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LEECreateView, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


class LEEUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """LEE entry UpdateView."""
    model = LEE
    form_class = UpdateLEEForm

    template_name = 'ops/support_lee_form.html'
    success_url = reverse_lazy('support-lee')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(LEEUpdateView, self).get_context_data(**kwargs)
        context['LEE_obj'] = LEE.objects.get(id=self.kwargs['pk'])
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


class LEEDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """LEE entry DeleteView."""
    model = LEE
    context_object_name = 'LEE'
    success_url = reverse_lazy('support-lee')
    template_name = 'ops/support_lee_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(LEEDeleteView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


# ####################### PEeP #######################
class PEePListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """PEeP ListView."""
    model = PEeP
    template_name = 'ops/support_peeps.html'
    context_object_name = 'peeps'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tasks'] = Task.objects.filter(assigned_user=self.request.user).exclude(task_status='Completed')
        # context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        context['search_off'] = True
        search_input = self.request.GET.get('search-area') or ''
        resp_search_input = self.request.GET.get('resp-search-area') or ''
        super_search_input = self.request.GET.get('super-search-area') or ''
        if search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(process_function__icontains=search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = search_input
            context['search_type'] = 'Function'
        if resp_search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(responsible__username__icontains=resp_search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = resp_search_input
            context['search_type'] = 'Resp'
        if super_search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(supervisor__username__icontains=super_search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = super_search_input
            context['search_type'] = 'Supervisor'

        context['search_input'] = search_input

        return context


class PEePDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """PEeP DetailView."""
    model = PEeP
    template_name = 'ops/support_peep_detail.html'
    context_object_name = 'peep'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(PEePDetailView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


class PEePCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """PEeP CreateView."""
    model = PEeP
    form_class = CreatePEePForm

    template_name = 'ops/support_peep_form.html'

    success_url = reverse_lazy('support-peeps')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        message = form.instance.process_function
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The PEeP entry "{message}" has been added.'
        )
        return super(PEePCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PEePCreateView, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


class PEePUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """PEeP entry UpdateView."""
    model = PEeP
    form_class = UpdatePEePForm

    template_name = 'ops/support_peep_form.html'
    success_url = reverse_lazy('support-peeps')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(PEePUpdateView, self).get_context_data(**kwargs)
        context['process_function'] = PEeP.objects.get(id=self.kwargs['pk']).process_function
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


class PEePDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """PEeP entry DeleteView."""
    model = PEeP
    context_object_name = 'peep'
    success_url = reverse_lazy('support-peeps')
    template_name = 'ops/support_peep_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(PEePDeleteView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context

