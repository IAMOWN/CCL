from django.urls import path

from .views import (
    ServiceGroupList,
    ServiceGroupDetail,
    ServiceGroupCreate,
    ServiceGroupUpdate,
    ServiceGroupDelete,
    ObjectiveList,
    ObjectiveDetail,
    ObjectiveCreate,
    ObjectiveUpdate,
    ObjectiveDelete,
)

urlpatterns = [
    # Service Groups
    path('service_groups/', ServiceGroupList.as_view(), name='service-groups'),
    path('service_group/<int:pk>/', ServiceGroupDetail.as_view(), name='service-group'),
    path('service_group_create/', ServiceGroupCreate.as_view(), name='service-group-create'),
    path('service_group_update/<int:pk>/', ServiceGroupUpdate.as_view(), name='service-group-update'),
    path('service_group_delete/<int:pk>/', ServiceGroupDelete.as_view(), name='service-group-delete'),

    # Objectives
    path('objectives/', ObjectiveList.as_view(), name='objectives'),
    path('objective/<int:pk>/', ObjectiveDetail.as_view(), name='objective'),
    path('objective_create/', ObjectiveCreate.as_view(), name='objective-create'),
    path('objective_update/<int:pk>/', ObjectiveUpdate.as_view(), name='objective-update'),
    path('objective_delete/<int:pk>/', ObjectiveDelete.as_view(), name='objective-delete'),
]
