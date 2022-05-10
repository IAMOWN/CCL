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
    Task,
    LEE,
    PEeP,
)

from .forms import (
    CreateServiceGroupForm,
    UpdateServiceGroupForm,
    CreateObjectiveForm,
    UpdateObjectiveForm,
    CreateTaskForm,
    UpdateTaskForm,
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
        service_group_objectives = Objective.objects\
            .filter(service_group=service_group)\
            .exclude(objective_status='3) Complete')\
            .exclude(objective_status='Cancelled')
        context['objectives'] = service_group_objectives

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
        objective = Objective.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Objective: {objective.objective}"
        tasks = Task.objects\
            .filter(objective=objective)\
            .exclude(task_status='Completed').order_by('task_status', '-due_date')
        context['tasks'] = tasks
        context['tasks_count'] = tasks.count()

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


# ####################### TASK VIEWS #######################
class TaskList(LoginRequiredMixin, ListView):
    """Task ListView for user's tasks."""
    model = Task
    template_name = 'ops/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['tasks_count'] = Task.objects.all().exclude(task_status='Completed').count()
        context['completed_tasks_count'] = Task.objects.filter(task_status='Completed').count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(task_title__icontains=search_input)  # Can also use __startswith
        context['search_input'] = search_input

        context['search_off'] = True
        assignee_search_input = self.request.GET.get('assignee-search-area') or ''
        task_search_input = self.request.GET.get('task-search-area') or ''
        status_search_input = self.request.GET.get('status-search-area') or ''
        priority_search_input = self.request.GET.get('priority-search-area') or ''
        context['search_count'] = 0
        if assignee_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(assigned_user__username=assignee_search_input)
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Assignee'
            context['search_entered'] = assignee_search_input
        elif task_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(task_title__icontains=task_search_input)
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Task'
            context['search_entered'] = task_search_input
        elif status_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(task_status__icontains=status_search_input)
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Status'
            context['search_entered'] = status_search_input
        elif priority_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(task_priority__icontains=priority_search_input)
            context['search_count'] = context['tasks'].exclude(task_status='Completed').count()
            context['search_type'] = 'Priority'
            context['search_entered'] = priority_search_input

        return context


# ####################### Task - Completed View #######################
class TaskCompletedList(LoginRequiredMixin, ListView):
    """Task ListView for user's completed tasks."""
    model = Task
    template_name = 'ops/tasks_completed.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['tasks'] = Task.objects.all().filter(task_status='Completed')
        context['completed_tasks_count'] = Task.objects.filter(task_status='Completed').count()
        context['tasks_count'] = Task.objects.all().exclude(task_status='Completed').count()

        return context


# ####################### Task - Customer Survey List View #######################
class TaskCustomerSurveyList(LoginRequiredMixin, ListView):
    """Task ListView for user's completed tasks."""
    model = Task
    template_name = 'ops/tasks_customer_survey.html'
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['surveys'] = Task.objects.all()\
            .filter(assigned_user=self.request.user)\
            .filter(task_type='Survey')\
            .exclude(task_status='Completed')
        context['survey_count'] = Task.objects.all()\
            .filter(assigned_user=self.request.user)\
            .filter(task_type='Survey')\
            .exclude(task_status='Completed')\
            .count()

        return context


# ####################### Task - Detail View #######################
class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task DetailView for user's tasks."""
    model = Task
    template_name = 'ops/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Survey Detail View #######################
class TaskSurveyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task Survey DetailView for user's tasks."""
    model = Task
    template_name = 'ops/task_detail_survey.html'
    context_object_name = 'task'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskSurveyDetail, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Create View #######################
class TaskCreate(LoginRequiredMixin, CreateView):
    """Task CreateView for user's tasks."""
    model = Task
    form_class = CreateTaskForm

    template_name = 'ops/task_form.html'

    def form_valid(self, form):
        form.instance.assigned_user = self.request.user
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been added'
        )
        return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Update View #######################
class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task UpdateView for user's tasks."""
    model = Task
    form_class = UpdateTaskForm

    template_name = 'ops/task_form.html'

    def form_valid(self, form):
        form.instance.assigned_user = self.request.user
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been updated'
        )
        return super(TaskUpdate, self).form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user or self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Survey Update View #######################
class TaskSurveyUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task Survey UpdateView."""
    model = Task
    fields = [
        'response_satisfaction',
        'response_comments',
    ]

    template_name = 'ops/task_form_survey.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        if form.instance.response_satisfaction == '2) Neutral':
            if form.instance.response_comments == '':
                form.add_error(
                    'response_comments',
                    'Please let us know why you rated your experience as 2) Neutral.'
                )
                return self.form_invalid(form)
        if form.instance.response_satisfaction == '3) Thumbs down':
            if form.instance.response_comments == '':
                form.add_error(
                    'response_comments',
                    'At Whurthy we are very serious about every customer realizing a breakthrough experience. '
                    'Please let us know why you rated your experience as 3) Thumbs down.'
                )
                return self.form_invalid(form)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for completing our Support survey.'
        )
        # support_object = Support.objects.get(id=form.instance.support_fk_id)
        # support_object.response_satisfaction = form.instance.response_satisfaction
        # support_object.response_comments = form.instance.response_comments
        if form.instance.response_satisfaction == '1) Thumbs up':
            response_score = 100.0
        elif form.instance.response_satisfaction == '2) Neutral':
            response_score = 50.0
        else:
            response_score = 0.0
        # support_object.response_score = response_score
        # support_object.save()
        form.instance.task_status = 'Completed'
        form.save()

        return super(TaskSurveyUpdate, self).form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskSurveyUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Cancel Request Update View #######################
class TaskCancelRequestUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task Cancel Request UpdateView."""
    model = Task
    fields = [
        'cancel_request_decision',
        'cancel_request_decision_comments',
        'cancellation_reason',
    ]

    template_name = 'ops/task_form_cancel_request.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        if form.instance.cancel_request_decision == '---':
            form.add_error(
                'cancel_request_decision',
                'Please select an outcome.'
            )
            return self.form_invalid(form)
        if form.instance.cancel_request_decision_comments == '':
            form.add_error(
                'cancel_request_decision_comments',
                'Please either enter the reason for decline or instructions for approval.'
            )
            return self.form_invalid(form)
        if form.instance.cancellation_reason == '':
            form.add_error(
                'cancellation_reason',
                'Please enter a cancellation reason. This will be used as a part of automated Email/Text notifications.'
            )
            return self.form_invalid(form)
        if form.instance.cancellation_reason == '':
            form.add_error(
                'cancellation_reason',
                'Please enter a cancellation reason. This will be used as a part of automated Email/Text notifications.'
            )
            return self.form_invalid(form)

        # if form.instance.cancel_request_decision == 'Approved':
        #     # cancellation_request = CancelHostVenue.objects.get(id=form.instance.cancel_host_venue.id)
        #     # cancellation_request.cancellation_status = '2) Approved'
        #     # cancellation_request.save(update_fields=['cancellation_status'])
        #     # request_period_start = cancellation_request.cancel_events_from
        #     # request_period_end = cancellation_request.cancel_events_to
        #     # host = cancellation_request.host
        #     # venue = cancellation_request.venue
        #     related_task_id = self.kwargs['pk']
        #     related_task = Task.objects.get(id=related_task_id)
        #
        #     # Create task - need to build branches for host and venue
        #     event_bookings_in_period = []
        #     total_deposits_paid = 0
        #     total_tax_collected = 0
        #     total_amount_due = 0
        #     total_amount_paid = 0
        #     # If this is Cancel For Host
        #
        #     # TODO V2 Build task text as a grid?
        #     # if host:
        #     #     event_bookings = EventBooking.objects.filter(
        #     #         event_start__gte=request_period_start,
        #     #         event_start__lte=request_period_end,
        #     #         host=host,
        #     #     ).exclude(
        #     #         booking_status='Cancelled'
        #     #     ).exclude(
        #     #         booking_status='4) Complete'
        #     #     ).order_by('event')
        #     #     events = Event.objects.filter(
        #     #         event_start__gte=cancellation_request.cancel_events_from,
        #     #         event_start__lte=cancellation_request.cancel_events_to,
        #     #         event_host=host,
        #     #     ).exclude(event_status='Cancelled')
        #     #     events_count = events.count()
        #     #
        #     #     event_bookings_in_period.append(
        #     #         f"""<h5><strong>Request Information</strong></h5><strong>Host: </strong>{host.host_name}<br><strong>Request Reference: </strong>{cancellation_request.request_reference}<br><strong>Requested by: </strong>{cancellation_request.cancellation_request_entered_by.profile.first_name} {cancellation_request.cancellation_request_entered_by.profile.last_name}<br><strong>Time Requested: </strong> {cancellation_request.cancellation_request_registered}<br><strong>Cancellation Reason:</strong><br>{form.instance.cancellation_reason}<br>"""
        #     #     )
        #     #     for booking in event_bookings:
        #     #         start_datetime = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #     #         start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M")
        #     #         if booking.customer.profile.notification_preference == 'None':
        #     #             notification_colour = 'text-danger'
        #     #         else:
        #     #             notification_colour = 'text-BlueGray'
        #     #         if booking.customer.profile.loyalty_tier == 'VIP':
        #     #             event_bookings_in_period.append(
        #     #                 f"""<br><strong>Event: </strong>{booking.event}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><span class='text-success'><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br></span><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #     #             )
        #     #         elif booking.customer.profile.loyalty_tier == 'Member':
        #     #             event_bookings_in_period.append(
        #     #                 f"""<br><strong>Event: </strong>{booking.event}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><span class='text-BlueGray'><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br></span><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #     #             )
        #     #         elif booking.customer.profile.loyalty_tier == 'Guest':
        #     #             event_bookings_in_period.append(
        #     #                 f"""<br><strong>Event: </strong>{booking.event}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #     #             )
        #     #         total_deposits_paid += booking.deposit_paid
        #     #         total_tax_collected += booking.total_tax
        #     #         total_amount_due += booking.total_amount_due
        #     #         total_amount_paid += booking.amount_paid
        #     #
        #     #     # Build description for events without bookings to be cancelled
        #     #     event_with_no_booking_header_flag = False
        #     #     for event in events:
        #     #         event_bookings_for_event = EventBooking.objects.filter(
        #     #             event=event,
        #     #             event_start__gte=cancellation_request.cancel_events_from,
        #     #             event_start__lte=cancellation_request.cancel_events_to,
        #     #             host=host,
        #     #         ).exclude(booking_status='Cancelled')
        #     #         # Build header for events without bookings that will still be cancelled
        #     #         if not event_with_no_booking_header_flag:
        #     #             event_bookings_in_period.append(
        #     #                 f"""<p><h5><strong>Events Without Bookings To Be Cancelled</strong></h5>"""
        #     #             )
        #     #             event_with_no_booking_header_flag = True
        #     #         # Add unbooked event to the description
        #     #         if event_bookings_for_event.count() == 0:
        #     #             event_bookings_in_period.append(
        #     #                 f"""<p><strong>Event: </strong>{event.event_name}</p>"""
        #     #             )
        #     #
        #     #     event_bookings_in_period.append(
        #     #         f"""<p><h5><strong>Event Booking Totals</strong></h5><strong>Total Deposits Paid: </strong>{total_deposits_paid}</p><p><strong>Total Tax: </strong>{total_tax_collected}</p><p><strong>Total Amount Due: </strong>{total_amount_due}</p><p><strong>Total Refunds: </strong>{total_amount_paid}</p>"""
        #     #     )
        #     #     create_host_cancellation_action_task(host, cancellation_request, event_bookings_in_period, related_task,form.instance.cancellation_reason)
        #     #
        #     #     messages.add_message(
        #     #         self.request,
        #     #         messages.SUCCESS,
        #     #         'The cancellation request has been marked as Approved, and will now be assigned to be completed by the Cancellation Coordinator.'
        #     #     )
        #     #     form.instance.task_status = 'Completed'
        #     #     form.instance.task_title = form.instance.task_title + ' [APPROVED]'
        #     #     form.save()
        #     # If this is Cancel For Venue
        #     else:
        #         event_bookings = EventBooking.objects.filter(
        #             event_start__gte=request_period_start,
        #             event_start__lte=request_period_end,
        #             venue=venue,
        #         ).exclude(
        #             booking_status='Cancelled'
        #         ).exclude(
        #             booking_status='4) Complete'
        #         ).order_by('event')
        #         events = Event.objects.filter(
        #             event_start__gte=request_period_start,
        #             event_start__lte=request_period_end,
        #             venue=venue,
        #         ).exclude(event_status='Cancelled')
        #         events_count = events.count()
        #
        #         event_bookings_in_period.append(
        #             f"""<h5><strong>Request Information</strong></h5><strong>Venue: </strong>{venue.event_venue}<br><strong>Request Reference: </strong>{cancellation_request.request_reference}<br><strong>Requested by: </strong>{cancellation_request.cancellation_request_entered_by.profile.first_name} {cancellation_request.cancellation_request_entered_by.profile.last_name}<br><strong>Time Requested: </strong> {cancellation_request.cancellation_request_registered}<br><strong>Cancellation Reason:</strong><br>{form.instance.cancellation_reason}<br>"""
        #         )
        #         for booking in event_bookings:
        #             start_datetime = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #             start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M")
        #             if booking.customer.profile.notification_preference == 'None':
        #                 notification_colour = 'text-danger'
        #             else:
        #                 notification_colour = 'text-BlueGray'
        #             if booking.customer.profile.loyalty_tier == 'VIP':
        #                 event_bookings_in_period.append(
        #                     f"""<br><strong>Event: </strong>{booking.event}<br><strong>Host: </strong>{booking.host}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><span class='text-success'><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br></span><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #                 )
        #             elif booking.customer.profile.loyalty_tier == 'Member':
        #                 event_bookings_in_period.append(
        #                     f"""<br><strong>Event: </strong>{booking.event}<br><strong>Host: </strong>{booking.host}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><span class='text-BlueGray'><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br></span><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #                 )
        #             elif booking.customer.profile.loyalty_tier == 'Guest':
        #                 event_bookings_in_period.append(
        #                     f"""<br><strong>Event: </strong>{booking.event}<br><strong>Host: </strong>{booking.host}<br><strong>Booking Status: </strong>{booking.booking_status}<br><strong>Customer: </strong>{booking.customer.profile.first_name} {booking.customer.profile.last_name}<br><strong>Phone: </strong>{booking.customer.profile.phone}<br><strong>Email: </strong>{booking.customer.email}<br><strong>Customer Loyalty Tier: </strong>{booking.customer.profile.loyalty_tier}<br><span class='{notification_colour}'><strong>Customer Notification Preference: </strong>{booking.customer.profile.notification_preference}</span><br><strong>Booking Start Time: </strong>{start_datetime}<br><strong>Regular Cost: </strong>{booking.event_regular_cost}<br><strong>Event Discount: </strong>{booking.event_discount}<br><strong>Discounted Event Cost: </strong>{booking.discounted_event_cost}<br><strong>Deposit Paid: </strong>{booking.deposit_paid}<br><strong>Total Tax: </strong>{booking.total_tax}<br><strong>Total Amount Due: </strong>{booking.total_amount_due}<br><strong>Amount Paid: </strong>{booking.amount_paid}<br><strong>Attended: </strong>{booking.attended}<br>"""
        #                 )
        #             total_deposits_paid += booking.deposit_paid
        #             total_tax_collected += booking.total_tax
        #             total_amount_due += booking.total_amount_due
        #             total_amount_paid += booking.amount_paid
        #
        #         # Build description for events without bookings to be cancelled
        #         event_with_no_booking_header_flag = False
        #         for event in events:
        #             event_bookings_for_event = EventBooking.objects.filter(
        #                 event=event,
        #                 event_start__gte=request_period_start,
        #                 event_start__lte=request_period_end,
        #                 venue=venue,
        #             )
        #             # Build header for events without bookings that will still be cancelled
        #             if not event_with_no_booking_header_flag:
        #                 event_bookings_in_period.append(
        #                     f"""<p><h5><strong>Events Without Bookings To Be Cancelled</strong></h5>"""
        #                 )
        #                 event_with_no_booking_header_flag = True
        #             # Add unbooked event to the description
        #             if event_bookings_for_event.count() == 0:
        #                 event_bookings_in_period.append(
        #                     f"""<p><strong>Event: </strong>{event.event_name}</p>"""
        #                 )
        #
        #         event_bookings_in_period.append(
        #             f"""<p><h5><strong>Event Booking Totals</strong></h5><strong>Total Deposits Paid: </strong>{total_deposits_paid}</p><p><strong>Total Tax: </strong>{total_tax_collected}</p><p><strong>Total Amount Due: </strong>{total_amount_due}</p><p><strong>Total Refunds: </strong>{total_amount_paid}</p>"""
        #         )
        #         create_venue_cancellation_action_task(venue, cancellation_request, event_bookings_in_period, related_task,form.instance.cancellation_reason)
        #
        #         messages.add_message(
        #             self.request,
        #             messages.SUCCESS,
        #             'The cancellation request has been marked as Approved, and will now be assigned to be completed by the Cancellation Coordinator.'
        #         )
        #         form.instance.task_status = 'Completed'
        #         form.instance.task_title = form.instance.task_title + ' [APPROVED]'
        #         # form.save()
        # else:
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request has been marked as Declined. No further action will be taken.'
        #     )
        #     form.instance.task_status = 'Completed'
        #     form.instance.task_title = form.instance.task_title + ' [DECLINED]'
        #     form.save()
        return super(TaskCancelRequestUpdate, self).form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCancelRequestUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context


# ####################### Task - Cancel Request Action Update View #######################
class TaskCancelRequestActionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task Cancel Request Action UpdateView."""
    model = Task
    fields = [
        'cancel_request_actions_taken',
        'cancel_request_notification',
        'cancel_request_cancellation',
        'task_status',
    ]

    template_name = 'ops/task_form_cancel_request_action.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCancelRequestActionUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
        context['year'] = get_current_year()

        return context

    # def form_valid(self, form):
        # if form.instance.cancel_request_actions_taken == '':
        #     form.add_error(
        #         'cancel_request_actions_taken',
        #         'Please enter the actions taken so far. Use this field to track what you have and and plan to do for this task.'
        #     )
        #     return self.form_invalid(form)
        # form.save(commit=False)
        #
        # # Get event bookings for notification and cancellations
        # cancel_obj = CancelHostVenue.objects.get(id=form.instance.cancel_host_venue.id)
        # # start_datetime = cancel_obj.cancel_events_from + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        # # end_datetime = cancel_obj.cancel_events_to + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        # start_datetime = cancel_obj.cancel_events_from
        # end_datetime = cancel_obj.cancel_events_to
        #
        # # Get event bookings and events to cancel for hosts
        # if cancel_obj.host:
        #     event_bookings = EventBooking.objects.filter(
        #         event_start__gte=start_datetime,
        #         event_start__lte=end_datetime,
        #         host=cancel_obj.host,
        #     ).exclude(
        #         booking_status='Cancelled'
        #     ).exclude(
        #         booking_status='4) Complete'
        #     ).order_by('event')
        #     events = Event.objects.filter(
        #         event_start__gte=cancel_obj.cancel_events_from,
        #         event_start__lte=cancel_obj.cancel_events_to,
        #         event_host=cancel_obj.host,
        #     ).exclude(event_status='Cancelled')
        #     events_count = events.count()
        # # Get event bookings and events to cancel for venues
        # else:
        #     event_bookings = EventBooking.objects.filter(
        #         event_start__gte=start_datetime,
        #         event_start__lte=end_datetime,
        #         venue=cancel_obj.venue,
        #     ).exclude(
        #         booking_status='Cancelled'
        #     ).exclude(
        #         booking_status='4) Complete'
        #     ).order_by('event')
        #     events = Event.objects.filter(
        #         event_start__gte=start_datetime,
        #         event_start__lte=end_datetime,
        #         venue=cancel_obj.venue,
        #     ).exclude(event_status='Cancelled')
        #     events_count = events.count()
        #
        # booking_count = event_bookings.count()
        # automated_activity_log = form.instance.automated_activity
        #
        # # (0) Check to see if there are events/bookings that can be cancelled. This will auto-complete the task.
        # if booking_count == 0 and not form.instance.automation_booking_cancel_flag and not form.instance.cancel_request_cancellation and events_count == 0:
        #     automated_activity_log = automated_activity_log + f'>>> There are no bookings or events in the system between {start_datetime.strftime("%d %b %Y %I:%M %p")} and {end_datetime.strftime("%d %b %Y %I:%M %p")} for Whurthy to automatically cancel. This task status has been marked as Completed.<br>'
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         f'There are no bookings or events in the system between {start_datetime.strftime("%d %b %Y %I:%M %p")} and {end_datetime.strftime("%d %b %Y %I:%M %p")} for Whurthy to automatically cancel. This task status has been automatically marked as Completed.'
        #     )
        #     form.instance.task_status = 'Completed'
        #     form.instance.automated_activity = automated_activity_log
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # notification_time = get_utc_datetime() + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #
        # # This branch allows for the task to updated after automation has already been triggered
        # if form.instance.cancel_request_cancellation and form.instance.automation_booking_cancel_flag:
        #     # automated_activity_log = automated_activity_log + f'>>> The cancellation request follow up action task has been updated.<br>'
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request follow up action task has been updated.'
        #     )
        #     # form.instance.automated_activity = automated_activity_log
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # # (1) Both automation branches blank
        # elif form.instance.cancel_request_cancellation == '---' and form.instance.cancel_request_notification == '---':
        #     # automated_activity_log = automated_activity_log + f'>>> The cancellation request follow up action task has been updated with both automation fields blank.<br>'
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request follow up action task has been updated.'
        #     )
        #     # form.instance.automated_activity = automated_activity_log
        #     form.instance.task_status = '2) In progress'
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # # (2) Manual notification and blank booking
        # elif form.instance.cancel_request_notification == 'Manual Notification' and form.instance.cancel_request_cancellation == '---':
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request follow up action task has been updated. This task is currently set for manual followup with customers about their cancelled event bookings.'
        #     )
        #     form.instance.task_status = '2) In progress'
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # # (4) Manual booking and blank notification
        # elif form.instance.cancel_request_cancellation == 'Manual Booking Cancellation' and form.instance.cancel_request_notification == '---':
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request follow up action task has been updated. This task is currently set to the manual cancellation of event bookings and events. Please be sure you are comfortable with manually cancelling events and bookings.'
        #     )
        #     form.instance.task_status = '2) In progress'
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # # (5) Both automation branches selected as Manual
        # elif form.instance.cancel_request_notification == 'Manual Notification' and form.instance.cancel_request_cancellation == 'Manual Booking Cancellation':
        #     automated_activity_log = automated_activity_log + f'>>> The cancellation request follow up action task has been updated with [Manual] set for both automation fields.<br>'
        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         'The cancellation request follow up action task has been updated. This task is currently set for manual followup with customers about their cancelled event bookings, and the manual cancellation of events and event bookings. Please be sure you are comfortable with manually cancelling events and bookings.'
        #     )
        #     form.instance.automated_activity = automated_activity_log
        #     # form.instance.task_status = '2) In progress'
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #
        # # (3 & 6 & 7 & 9) Automated notification and manual booking - least preferred
        # elif form.instance.cancel_request_notification == 'Automated Notification' and not form.instance.automation_email_flag and not form.instance.automation_sms_flag:
        #     # (6)
        #     if form.instance.cancel_request_cancellation == 'Manual Booking Cancellation':
        #         email_count = 0
        #         sms_count = 0
        #         for booking in event_bookings:
        #             if booking.customer.profile.notification_preference == 'Email' and not form.instance.automation_email_flag:
        #                 automated_activity_log = automated_activity_log + f'>>> Email sent to {booking.event_booked_by.profile.first_name} {booking.event_booked_by.profile.last_name} to the email address {booking.event_booked_by.email} at {notification_time.strftime("%d %b %Y %I:%M %p")}.<br>'
        #                 start_time = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #
        #                 cancellation_email_notification(start_time, booking, form)
        #                 form.instance.automation_email_flag = True
        #                 form.instance.automation_notification_flag = True
        #                 email_count += 1
        #             elif booking.customer.profile.notification_preference == 'Text/SMS' and settings.SMS_MESSAGING_SERVICE == 'BulkSMS' and not form.instance.automation_sms_flag:
        #                 automated_activity_log = automated_activity_log + f'>>> Text sent to {booking.event_booked_by.profile.first_name} {booking.event_booked_by.profile.last_name} to the number {booking.event_booked_by.profile.phone} at {notification_time.strftime("%d %b %Y %I:%M %p")}.<br>'
        #                 sms_event_start = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #                 sms_to_phone = str({booking.customer.profile.phone.raw_phone})
        #                 sms_to_phone = sms_to_phone.replace("+", "")
        #                 sms_to_phone = sms_to_phone.replace("""'}""", "")
        #                 sms_to_phone = sms_to_phone.replace("""{'""", "")
        #                 sms_body = f'''We regret to inform you that your booking on {sms_event_start.strftime("%A, %d %b %Y")} at {sms_event_start.strftime("%I:%M %p")} for the event, "{booking.event}" has been cancelled for the reason, {form.instance.cancellation_reason}\nPlease accept our apologies and do not hesitate to contact us at {settings.COMPANY_PHONE} with any questions you may have.'''
        #                 cancellation_sms_notification(sms_to_phone, sms_body, sms_to_phone)
        #                 sms_count += 1
        #                 form.instance.automation_sms_flag = True
        #                 form.instance.automation_notification_flag = True
        #         automated_activity_log = automated_activity_log + f'<span class="text-danger">>>> WARNING: Manual booking cancellation is the selection that brings with it the most risk for process failure. You are recommended to proceed with caution.</span><br>'
        #         form.instance.automated_activity = automated_activity_log
        #         form.instance.task_status = '2) In progress'
        #         form.save()
        #         messages.add_message(
        #             self.request,
        #             messages.SUCCESS,
        #             'WARNING: Manual booking cancellation is the selection that brings with it the most risk for process failure. You are recommended to proceed with caution.'
        #         )
        #         return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #     # (3)
        #     elif form.instance.cancel_request_notification == '---':
        #         # (9) Notification not necessary
        #         if booking_count == 0:
        #             automated_activity_log = automated_activity_log + f'>>> There are no bookings, and thus automated notification is not required.<br>'
        #             form.instance.cancel_request_notification = 'Automated Notification'
        #             form.instance.automation_notification_flag = True
        #             form.instance.automation_booking_cancel_flag = True
        #             form.instance.automated_activity = automated_activity_log
        #             form.save()
        #             return super(TaskCancelRequestActionUpdate, self).form_valid(form)
        #         # (7) There are bookings, so require notification to be set
        #         else:
        #             automated_activity_log = automated_activity_log + f'>>> There are bookings. A notification preference is required. Error returned.<br>'
        #             form.instance.automated_activity = automated_activity_log
        #             form.save()
        #             form.add_error(
        #                 'cancel_request_notification',
        #                 'Automating booking cancellation requires that a notification approach be selected. '
        #                 'We recommend triggering automated notifications when cancellations are automated. '
        #                 'However, it is possible to automatically cancel events and then manually notify customers.'
        #             )
        #             return self.form_invalid(form)
        #
        # # (7 & 8 & 9) Automated cancellation with notification - 0 bookings completes, or returns invalid form. With bookings a selection must be made.
        # elif form.instance.cancel_request_cancellation == 'Automated Booking Cancellation' and not form.instance.automation_booking_cancel_flag:
        #     if form.instance.cancel_request_notification == '---' and not form.instance.automation_notification_flag:
        #         # (9) Notification not necessary
        #         if booking_count == 0:
        #             automated_activity_log = automated_activity_log + f'>>> There are no bookings, and thus automated notification is not required.<br>'
        #             form.instance.cancel_request_notification = 'Automated Notification'
        #             form.instance.automation_notification_flag = True
        #             form.instance.automation_booking_cancel_flag = True
        #             form.instance.automated_activity = automated_activity_log
        #             form.save(commit=False)
        #         # (7) There are bookings, so require notification to be set
        #         else:
        #             automated_activity_log = automated_activity_log + f'>>> There are bookings. A notification preference is required. Error returned.<br>'
        #             form.instance.automated_activity = automated_activity_log
        #             form.save()
        #             form.add_error(
        #                 'cancel_request_notification',
        #                 'Automating booking cancellation requires that a notification approach be selected. '
        #                 'We recommend triggering automated notifications when cancellations are automated. '
        #                 'However, it is possible to automatically cancel events and then manually notify customers.'
        #             )
        #             return self.form_invalid(form)
        #
        #     # If automated notifications are selected AND there are bookings to cancel/notify
        #     email_count = 0
        #     sms_count = 0
        #     # (9) Auto booking and auto notifications
        #     if form.instance.cancel_request_notification == 'Automated Notification' and booking_count > 0:
        #         # Send emails and/or texts if there are bookings
        #         for booking in event_bookings:
        #             if booking.customer.profile.notification_preference == 'Email' and not form.instance.automation_email_flag:
        #                 automated_activity_log = automated_activity_log + f'>>> Email sent to {booking.event_booked_by.profile.first_name} {booking.event_booked_by.profile.last_name} to the email address {booking.event_booked_by.email} at {notification_time.strftime("%d %b %Y %I:%M %p")}.<p>'
        #                 start_time = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #
        #                 cancellation_email_notification(start_time, booking, form)
        #                 form.instance.automation_email_flag = True
        #                 form.instance.automation_notification_flag = True
        #                 email_count += 1
        #             elif booking.customer.profile.notification_preference == 'Text/SMS' and settings.SMS_MESSAGING_SERVICE == 'BulkSMS' and not form.instance.automation_sms_flag:
        #                 automated_activity_log = automated_activity_log + f'>>> Text sent to {booking.event_booked_by.profile.first_name} {booking.event_booked_by.profile.last_name} to the number {booking.event_booked_by.profile.phone} at {notification_time.strftime("%d %b %Y %I:%M %p")}.<p>'
        #                 sms_event_start = booking.event_start + timedelta(hours=settings.SMS_TIME_ZONE_SEND_CONVERSION)
        #                 sms_to_phone = str({booking.customer.profile.phone.raw_phone})
        #                 sms_to_phone = sms_to_phone.replace("+", "")
        #                 sms_to_phone = sms_to_phone.replace("""'}""", "")
        #                 sms_to_phone = sms_to_phone.replace("""{'""", "")
        #                 sms_body = f'''We regret to inform you that your booking on {sms_event_start.strftime("%A, %d %b %Y")} at {sms_event_start.strftime("%I:%M %p")} for the event, "{booking.event}" has been cancelled for the reason, {form.instance.cancellation_reason}\nPlease accept our apologies and do not hesitate to contact us at {settings.COMPANY_PHONE} with any questions you may have.'''
        #                 cancellation_sms_notification(sms_to_phone, sms_body, sms_to_phone)
        #                 sms_count += 1
        #                 form.instance.automation_sms_flag = True
        #                 form.instance.automation_notification_flag = True
        #         form.instance.automated_activity = automated_activity_log
        #
        #     # TODO V2 Add cancellation loss and impact to customer profile?
        #     # AUTOMATED BOOKING CANCELLATIONS
        #     bookings_cancelled = 0
        #     events_cancelled = 0
        #     form.instance.automation_booking_cancel_flag = True
        #     for booking in event_bookings:
        #         booking_to_cancel = EventBooking.objects.get(id=booking.id)
        #         booking_to_cancel.booking_status = 'Cancelled'
        #         booking_to_cancel.save(update_fields=['booking_status'])
        #         automated_activity_log = automated_activity_log + f'>>> Event Booking cancelled: {booking.booking_reference}<br>'
        #         bookings_cancelled += 1
        #
        #     for event in events:
        #         cancel_event = Event.objects.get(id=event.id)
        #         cancel_event.event_status = 'Cancelled'
        #         cancel_event.save(update_fields=['event_status'])
        #         events_cancelled += 1
        #         automated_activity_log = automated_activity_log + f'>>> Event cancelled: {cancel_event.event_name}<br>'
        #
        #     # (9) Browser message
        #     if form.instance.cancel_request_notification == 'Automated Notification':
        #         messages.add_message(
        #             self.request,
        #             messages.SUCCESS,
        #             f'The cancellation request follow up action task has been updated. NOTIFICATIONS: {email_count} email(s) and {sms_count} SMS message(s) were sent. CANCELLATIONS: {events_cancelled} event(s) and {bookings_cancelled} event booking(s) were cancelled by Whurthy.'
        #         )
        #     # (8) Auto booking and manual notifications
        #     else:
        #         messages.add_message(
        #             self.request,
        #             messages.SUCCESS,
        #             f'The cancellation request follow up action task has been updated. {events_cancelled} event(s) and {bookings_cancelled} event booking(s) were cancelled by Whurthy.'
        #         )
        #     form.instance.automated_activity = automated_activity_log
        #     # form.instance.task_status = '2) In progress'
        #     form.save()
        #     return super(TaskCancelRequestActionUpdate, self).form_valid(form)


# ####################### Task - Delete View #######################
class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Task DeleteView for user's tasks."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'ops/task_confirm_delete.html'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDelete, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()
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

