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
    ObjectiveServiceGroupCreate,
    ObjectiveUpdate,
    ObjectiveDelete,
    LEEListView,
    LEEDetailView,
    LEECreateView,
    LEEUpdateView,
    LEEDeleteView,
    PEePListView,
    PEePDetailView,
    PEePCreateView,
    PEePUpdateView,
    PEePDeleteView,
)

urlpatterns = [
    # LEE
    path('lee/', LEEListView.as_view(), name='support-lee'),
    path('lee/<int:pk>/', LEEDetailView.as_view(), name='support-lee-entry'),
    path('lee_create/', LEECreateView.as_view(), name='support-lee-create'),
    path('lee_update/<int:pk>/', LEEUpdateView.as_view(), name='support-lee-update'),
    path('lee_delete/<int:pk>/', LEEDeleteView.as_view(), name='support-lee-delete'),

    # PEeP
    path('peeps/', PEePListView.as_view(), name='support-peeps'),
    path('peep/<int:pk>/', PEePDetailView.as_view(), name='support-peep-entry'),
    path('peep_create/', PEePCreateView.as_view(), name='support-peep-create'),
    path('peep_update/<int:pk>/', PEePUpdateView.as_view(), name='support-peep-update'),
    path('peep_delete/<int:pk>/', PEePDeleteView.as_view(), name='support-peep-delete'),

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
    path('objective_create_for_service_group/<int:pk>/', ObjectiveServiceGroupCreate.as_view(), name='objective-create-for-service_group'),
    path('objective_update/<int:pk>/', ObjectiveUpdate.as_view(), name='objective-update'),
    path('objective_delete/<int:pk>/', ObjectiveDelete.as_view(), name='objective-delete'),
]
