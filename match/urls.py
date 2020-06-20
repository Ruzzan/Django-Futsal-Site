from django.urls import path
from .views import (
    CreateMatchView,
    MatchIndexView,
    MatchFixView,
    MatchSearchView
)

urlpatterns = [
    path('',MatchIndexView.as_view(),name='match-index'),
    path('create/',CreateMatchView.as_view(),name='match-create'),
    path('fix',MatchFixView.as_view(),name='match-fix'),
    path('search',MatchSearchView.as_view(),name='match-search'),
]