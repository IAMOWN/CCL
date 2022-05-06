from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

SERVICE_GROUP_TYPES = [
    ('---', '---'),
    ('1) Esoteric', '1) Esoteric'),
    ('2) Exoteric', '2) Exoteric'),
]
SERVICE_GROUP_STATUS = [
    ('1) Active', '1) Active'),
    ('2) Inactive', '2) Inactive'),
]


# ####################### Service Group #######################
class ServiceGroup(models.Model):
    """Groups users into related Service Groups."""
    service_group = models.CharField(
        max_length=150,
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
        auto_now=True
    )

    def __str__(self):
        return self.service_group

    class Meta:
        verbose_name_plural = 'Service Groups'
        verbose_name = 'Service Group'
