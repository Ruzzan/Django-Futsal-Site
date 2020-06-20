from django.urls import path
from .views import (TeamCreateView,
TeamDetailView,
TeamUpdateView,
JoinTeamView,
LeaveTeamView,
TeamDeleteView,
RemoveMemberView,
TeamIndexView,
TeamSearchView)

urlpatterns = [
    path('',TeamIndexView.as_view(),name='team-index'),
    path('create/',TeamCreateView.as_view(),name='team-create'),
    path('search',TeamSearchView.as_view(),name='team-search'),
    path('<slug:slug>',TeamDetailView.as_view(),name='team-detail'),
    path('update/<slug:slug>',TeamUpdateView.as_view(),name='team-update'),
    path('delete/<int:pk>/<slug:slug>',TeamDeleteView.as_view(),name='team-delete'),
    path('join/<slug:slug>/',JoinTeamView.as_view(),name='join-team'),
    path('leave/<slug:slug>/',LeaveTeamView.as_view(),name='leave-team'),
    path('remove/<slug:slug>/',RemoveMemberView.as_view(),name='remove-member'),
]