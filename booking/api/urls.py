from django.urls import path
from .views import BookingListAPI, BookingDetailAPI
urlpatterns = [
    path('',BookingListAPI.as_view(),name='booking-api'),
    path('<int:pk>/',BookingDetailAPI.as_view(),name='booking-detail')
]