from django.urls import path
from .views import TeamListAPI, TeamDetailAPI, TeamMemberListAPI, TeamMemberDetailAPI

urlpatterns = [
    path('',TeamListAPI.as_view(),name='team'),
    path('<int:pk>/',TeamDetailAPI.as_view(),name='team-detail'),
    path('members/',TeamMemberListAPI.as_view(),name='team-members'),
    path('members/<int:pk>/',TeamMemberDetailAPI.as_view(),name='team-member-detail')
]