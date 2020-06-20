from django.urls import path
from .views import FutsalListAPI, FutsalDetailAPI
urlpatterns = [
    path('',FutsalListAPI.as_view(),name='futsal'),
    path('<int:pk>/',FutsalDetailAPI.as_view(),name='futsal-detail'),
]