from django.urls import path
from .views import MatchListAPI, MatchDetailAPI, MatchObjectListAPI, MatchObjectDetailAPI

urlpatterns = [
    path('',MatchListAPI.as_view(),name='match'),
    path('<int:pk>/',MatchDetailAPI.as_view(),name='match-detail'),
    path('match/',MatchObjectListAPI.as_view(),name='matchobj-list'),
    path('match/<int:pk>/',MatchObjectDetailAPI.as_view(),name='matchobj-detail'),
]