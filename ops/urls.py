from django.urls import path

from .views import (
    ServiceGroupList,
    ServiceGroupDetail,
    ServiceGroupCreate,
    ServiceGroupUpdate,
    ServiceGroupDelete,
)

urlpatterns = [
    # Service Groups
    path('service_groups/', ServiceGroupList.as_view(), name='service-groups'),
    path('service_group/<int:pk>/', ServiceGroupDetail.as_view(), name='service-group'),
    path('service_group_create/', ServiceGroupCreate.as_view(), name='service-group-create'),
    path('service_group_update/<int:pk>/', ServiceGroupUpdate.as_view(), name='service-group-update'),
    path('service_group_delete/<int:pk>/', ServiceGroupDelete.as_view(), name='service-group-delete'),
]
