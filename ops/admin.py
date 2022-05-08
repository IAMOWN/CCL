from django.contrib import admin

from .models import (
    ServiceGroup,
    Objective,
)
admin.site.register(ServiceGroup)
admin.site.register(Objective)
