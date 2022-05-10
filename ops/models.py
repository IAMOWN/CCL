from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from tinymce.models import HTMLField

# ####################### CONSTANTS #######################
SERVICE_GROUP_TYPES = [
    ('---', '---'),
    ('1) Esoteric', '1) Esoteric'),
    ('2) Exoteric', '2) Exoteric'),
]
SERVICE_GROUP_STATUS = [
    ('1) Active', '1) Active'),
    ('2) Inactive', '2) Inactive'),
]
OBJECTIVE_DEVELOPMENT_CHOICES = [
    ('1) Simple', '1) Simple'),
    ('2) Descriptive', '2) Descriptive'),
    ('3) Change', '3) Change'),
]
OBJECTIVE_STATUS = [
    ('1) Not started', '1) Not started'),
    ('2) In progress', '2) In progress'),
    ('3) Deferred', '3) Deferred'),
    ('3) Complete', '3) Complete'),
    ('Cancelled', 'Cancelled'),
]
TASK_STATUS_CHOICES = [
    ('1) Not started', '1) Not started'),
    ('2) In progress', '2) In progress'),
    ('3) Deferred', '3) Deferred'),
    ('Completed', 'Completed'),
]
TASK_PRIORITY_CHOICES = [
    ('1) High', '1) High'),
    ('2) Normal', '2) Normal'),
    ('3) Low', '3) Low'),
]
TASK_TYPE_CHOICES = [
    ('---', '---'),
    ('Service Group', 'Service Group'),
    ('Objective', 'Objective'),
    ('Prepayment', 'Prepayment'),
    ('Wait List', 'Wait List'),
    ('Survey', 'Survey'),
    ('ALAN', 'ALAN'),
    ('Cancellation Request', 'Cancellation Request'),
    ('Cancellation Action', 'Cancellation Action'),
]
RESPONSE_SATISFACTION_CHOICES = [
    ('---', '---'),
    ('1) Thumbs up', '1) Thumbs up'),
    ('2) Neutral', '2) Neutral'),
    ('3) Thumbs down', '3) Thumbs down'),
]
YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No')
]
CANCEL_REQUEST_DECISION = [
    ('---', '---'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
]
CANCEL_REQUEST_AUTOMATION_NOTIFICATION_CHOICES = [
    ('---', '---'),
    ('Automated Notification', 'Automated Notification'),
    ('Manual Notification', 'Manual Notification'),
]
CANCEL_REQUEST_AUTOMATION_CANCELLATION_CHOICES = [
    ('---', '---'),
    ('Automated Booking Cancellation', 'Automated Booking Cancellation'),
    ('Manual Booking Cancellation', 'Manual Booking Cancellation'),
]
WHURTHY_TEAM_CHOICES = [
    ('Finance', 'Finance'),
    ('Operations', 'Operations'),
    ('People', 'People'),
    ('Product Management', 'Product Management'),
    ('Sales', 'Sales'),
    ('Support', 'Support'),
]
APPLICATION_CHOICES = [
    ('CCL', 'CCL'),
    ('Events', 'Events'),
    ('Ops', 'Ops'),
    ('Users', 'Users'),
    ('Other', 'Other'),
]


# ####################### Service Group #######################
class ServiceGroup(models.Model):
    """Groups users into related Service Groups."""
    service_group = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        default=''
    )
    members = models.ManyToManyField(User)
    purpose = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    qualified_intentions = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    service_group_type = models.CharField(
        max_length=20,
        choices=SERVICE_GROUP_TYPES,
        default='---'
    )
    service_group_status = models.CharField(
        max_length=20,
        choices=SERVICE_GROUP_STATUS,
        default='1) Active'
    )

    # Record metadata
    service_group_creator = models.ForeignKey(
        User,
        related_name='service_group_creator',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.service_group

    class Meta:
        verbose_name_plural = 'Service Groups'
        verbose_name = 'Service Group'
        ordering = [
            'service_group_type',
            'service_group',
        ]

    def get_absolute_url(self):
        return reverse('service-group', kwargs={'pk': self.pk})


# ####################### Objective #######################
class Objective(models.Model):
    """Objectives are set by Service Groups and can be parents to tasks."""
    objective = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        default=''
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        related_name='objective_service_group',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    objective_status = models.CharField(
        max_length=20,
        choices=OBJECTIVE_STATUS,
        default='1) Not started',
    )
    objective_development_template = models.CharField(
        max_length=20,
        choices=OBJECTIVE_DEVELOPMENT_CHOICES,
        default='1) Simple',
        help_text='''While a simple objective will only display a simple text field selecting "2) Complex" will open up 
        fields to capture an Opportunity and Objective Statement. Selecting "3) Change" will also open up fields to 
        support the Group in building a change management plan. Please remember that specific Tasks can be created for 
        Objectives. In this way, an Objective can have many Tasks. Many Tasks allow for the creation of a plan designed 
        to fulfill an Objective.'''
    )
    opportunity_statement = HTMLField(
        default='What is wrong, where it happened, when it occurred, to what extent, and we know because...',
        blank=True,
        null=True,
        help_text='''The purpose of an Opportunity Statement is to clearly define what needs to be changed. Ideally, it 
        can clearly and concisely communicate this opportunity to others. A well-crafted Opportunity Statement can 
        inspire groups to operate in Divine Economy and support Qualification with the 'I AM' Presence.\n
        A good Opportunity Statement describes "what" the challenge is, "where" the challenge is observed 
        geographically, when this challenge was first observed (history, patterns, etc.), "how much" the opportunity 
        has been a challenge (trends etc.), and "how we know" by clarifying the intention that has not been met.\n
        An example of a good Opportunity Statement would cover "What is wrong, where it happened, when it occurred, to 
        what extent, and we know because..."''',
    )
    objective_statement = HTMLField(
        default='SMART (Specific, Measurable, Achievable, Relevant, Timely) Objective...',
        blank=True,
        null=True,
        help_text='''An objective statement empowers a Group throughout the service activity. An essential question for 
        any group is to ask, Why is the accomplishment of this objective important to the EGA Divine Plan?\n
        Elements of an Objective Statement that will make it stronger are SMART: Specific (state what the Group will do)
        ; Measurable (provide a way to evaluate through metrics or data); Achievable (possible to accomplish, 
        attainable); Relevant (makes sense in the context of the EGA Divine Plan); Time-bound (states when the objective 
         will be accomplished).''',
    )
    awareness = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='''What is the awareness of the need for change? While there is yet some time before the human 
        collective will be able to see with the Fullness of God’s Vision, there are some questions that can be brought 
        to the ‘I AM’ Presence, and in turn that the Group can engage with.\n
        How will Divine Will be expressed as Purpose? How will Intentions be formed and Qualified? Why is this being 
        done?  How will the EGA Divine Plan be expanded? What is required to manifest this change? How will Thy Will 
        Be Done?''',
    )
    clarity = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='''Is there clarity to participate and support the change? When there is a shared awareness there 
        will be a number of potentials that typically unfold. Is the Group ready to participate and support the 
        change?  This is where engagement, or a lack of engagement, will be exposed (lack of Clarity is most definitely 
        the existing barrier amongst the EGA human collective). It is for the Group to take the time, with an 
        awareness of Divine Order, to truly ensure that all of the Group have Clarity. While there will come a time 
        when Christ Councils are functioning, and Clarity will follow the Light as a flower follows the Sun, for now we 
        are Building a Bridge.\n
        Clarity will not flow if there is an assumption that everyone understands.  The Group that takes time to 
        validate clarity is better for the effort.  You should neither under-estimate the power of information nor 
        forget that those that feel unheard will be less likely to engage.\n
        In short, the objective at this stage is to build a foundation through engagement that can truly begin to 
        emerge around the change.  Clarity involves everyone checking in with everyone present be sure ALL are clear 
        about what is being discussed, to make sure that everyone understands what the Group is being asked to Qualify. 
        This may take some time to adjust to at first.''',
    )
    emergence = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='''What knowledge and abilities are required for the change? With the foundation for the emergence of 
        engagement set in the previous phase, the Group can now build a momentum of engagement.  However, this is where 
        the symbiosis of both the Esoteric and Exoteric begin to really shine.  For ‘Thy Will to Be Done’, there will 
        be need for the Emergence of knowledge and ability.\n
        Useful Questions for Exoteric Groups (2) at this stage include: Will training and education be required? Do we 
        have sufficient detailed information about the Mystical Methods and Processes? Should they be templated? How 
        will they be Implemented? How will they evolve? Will new service responsibilities be needed? How will existing 
        service responsibilities be impacted?\n
        Additional questions for Groups to Contemplate and Qualify include: What is the current knowledge base of those 
        being asked to engage in this change? What is their capacity to gain additional knowledge? What existing 
        knowledge and information do we have access to? What educational resources will need to be made available? What 
        psychological blocks are already apparent amongst the Group? Remember, we are building a bridge! 
        Are there physical limitations to consider? Are there Dear Souls with Gifts that align to needed activities? 
        What time is anticipated to be needed to develop required skills? What financial resources, tools, and 
        materials will be required?''',
    )
    discipline = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='''What is required to sustain the change? How will we ensure that progress is communicated? Do we 
        have the appropriate accountability mechanisms in place?''',
    )

    # Record metadata
    objective_creator = models.ForeignKey(
        User,
        related_name='objective_creator',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return self.objective

    class Meta:
        verbose_name_plural = 'Objectives'
        verbose_name = 'Objective'
        ordering = [
            'service_group',
            'objective',
        ]

    def get_absolute_url(self):
        return reverse('objective', kwargs={'pk': self.pk})


# ####################### PEeP #######################
class PEeP(models.Model):
    """
    PEeP (Process Expertise Profile model. Captures Team members by function/responsibility for task
    assignment. Related to User as each entry relates to a Team member.
    """
    process_function = models.CharField(
        unique=True,
        max_length=50,
        default='',
        help_text='Enter the Team member job title or functional activity. Note: Whurthy will only be able to act on '
                  'this record if the applicable feature has been built into the application. However, please feel free '
                  'to enter PEeP records for your own reference, and to identify future automation opportunities.'
    )
    process_code = models.CharField(
        max_length=20,
        default='',
        help_text="Enter the process code for this process activity. The recommended format should be abbreviations of "
                  "the organization's name and the process name. For example, the Whurthy employee on-boarding "
                  "process could have the process code of LFON. There is a limit of 20 characters for the Process Code."
    )
    responsible = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    display_name = models.CharField(
        max_length=30,
        default='',
    )  # Display name may be redundant - replace with Profile.first_name and Profile.last_name
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='PEeP_entry_supervisor',
    )
    whurthy_team = models.CharField(
        max_length=50,
        choices=WHURTHY_TEAM_CHOICES,
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        related_name='PEeP_service_group',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    detailed_description = models.TextField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.process_function

    class Meta:
        ordering = [
            'whurthy_team',
            'process_code',
            'date_created',
        ]
        verbose_name_plural = 'PEeP'
        verbose_name = 'PEeP'


# ####################### LEE #######################
class LEE(models.Model):
    """
    Learned Experience Engine model. Captures process descriptions for tasks and form errors.
    """
    process_role = models.CharField(
        max_length=100,
        default='',
        unique=True,
        help_text='Enter the specific task name. This should not be changed once it has been coded into the Whurthy '
                  'application, as it will be used in task assignment.'
    )
    whurthy_application = models.CharField(
        max_length=100,
        default='CCL',
        choices=APPLICATION_CHOICES,
        help_text='Please select the application that this entry applies to.',
        verbose_name='CCL Application'
    )
    relevant_file = models.CharField(
        default='events/ views.py',
        max_length=100,
        null=True,
        blank=True,
        help_text='If applicable, enter the specific file path and file name.'
    )
    process_description = models.TextField(
        default='',
        help_text='Enter the process description for the task. Whatever is entered into this field will be the '
                  'process description provided for the task assignment/notification to the assignee.'
    )
    entry_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lEE_entry_owner'
    )
    process_code = models.CharField(
        max_length=10,
        default='WEVENT',
        help_text="Enter the process code for this process activity. The recommended format should be abbreviations of "
                  "the organization's name and the process name. For example, the Whurthy employee on-boarding "
                  "process could have the process code of WON. There is a limit of 10 characters for the Process Code."
    )
    process_outcome = models.TextField(
        null=True,
        blank=True,
        help_text='If applicable, enter a description of the outcome of the process.'
    )
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.process_role} ({self.whurthy_application})'

    class Meta:
        ordering = [
            'process_role'
        ]
        verbose_name_plural = 'LEE'
        verbose_name = 'LEE'


# ####################### Tasks #######################
class Task(models.Model):
    """Task model. Captures the independent tasks for any given user.
    Is only one of two apps that can be used without an Organization or Team created (by design).
    The idea is that a user may want to plan before building out the org structure. This would be particularly
    true for Consulting Agency users.
    Related to User/Profile as each task belongs to a user."""
    task_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        related_name='task_service_group',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    objective = models.ForeignKey(
        Objective,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Assigned to'
    )
    # event = models.ForeignKey(
    #     Event,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
    task_description = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    assigned_team = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default='',
        help_text='''
        If you have many teams collaborating in Whurthy you can enter in the Team name. This will allow you to 
        filter by team in the task list. 
        '''
    )
    task_status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default='1) Not started'
    )
    task_priority = models.CharField(
        max_length=20,
        choices=TASK_PRIORITY_CHOICES,
        default='2) Normal',
        help_text="Selecting '1) High' will not only place the task higher in the task list but will also "
                  "result in it showing in the 'My High Priority' section of the dashboard."
    )
    due_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        help_text='Enter the date you are aiming to complete this task by.'
    )
    task_type = models.CharField(
        choices=TASK_TYPE_CHOICES,
        max_length=50,
        default='---',
    )
    # support_fk = models.ForeignKey(
    #     Support,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
    response_satisfaction = models.CharField(
        max_length=20,
        choices=RESPONSE_SATISFACTION_CHOICES,
        default='---',
        help_text='How do you rate your support experience?'
    )
    response_comments = models.TextField(
        null=True,
        blank=True,
        help_text='Please share any specific feedback about your support experience.'
    )
    # cancel_host_venue = models.ForeignKey(
    #     CancelHostVenue,
    #     null=True,
    #     blank=True,
    #     related_name='cancelled_for_host_venue',
    #     on_delete=models.CASCADE
    # )
    cancellation_reason = models.TextField(
        null=True,
        blank=True,
        help_text='''What is the reason for this cancellation? Remember that the reason entered will be used as a part 
        of automatically notifying customers that their event booking has been cancelled.''',
    )
    cancel_request_decision = models.CharField(
        choices=CANCEL_REQUEST_DECISION,
        max_length=20,
        default='---',
    )
    cancel_request_decision_comments = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    cancel_request_actions_taken = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    cancel_request_notification = models.CharField(
        choices=CANCEL_REQUEST_AUTOMATION_NOTIFICATION_CHOICES,
        max_length=40,
        default='---',
        help_text='''Selecting <Automated Notification> will result in all customers with the Notification Preference 
        of SMS or Email being automatically notified. You will need to follow up with those Customers who have None 
        as their Notification Preference. If you select <Manual Notification> it assumed you will notify each customer 
        of their cancelled booking.'''
    )
    cancel_request_cancellation = models.CharField(
        choices=CANCEL_REQUEST_AUTOMATION_CANCELLATION_CHOICES,
        max_length=40,
        default='---',
        help_text='''Selecting <Automated Booking Cancellation> will result all listed events and event bookings set 
        to the status of cancelled. If you select <Manual Booking Cancellation> it assumed you will manually cancel the 
        event and all associated event bookings.'''
    )
    automated_activity = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    automation_email_flag = models.BooleanField(default=False)
    automation_sms_flag = models.BooleanField(default=False)
    automation_notification_flag = models.BooleanField(default=False)
    automation_booking_cancel_flag = models.BooleanField(default=False)
    related_task = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='approval_task',
        on_delete=models.CASCADE
    )

    task_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task_title} ** Status - {self.task_status} ({self.id})'

    class Meta:
        ordering = [
            'task_status',
            'task_priority',
            'due_date',
        ]

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})
