from django.urls import path
from .views import (HomePageView,
FutsalListView,
FutsalDetailView,
FutsalUpdateView,
FutsalSearchView
)
urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('list/',FutsalListView,name='futsal-list'),
    path('search',FutsalSearchView,name='futsal-search'),
    path('<slug:slug>/',FutsalDetailView,name='futsal-detail'),
    path('edit/<slug:slug>/',FutsalUpdateView.as_view(),name='futsal-edit'),
]