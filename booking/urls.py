from django.urls import path
from .views import CreateBookingView, OwnerDashboardView, OwnerDashboardSearchView, DeleteBooking
urlpatterns = [
    path('',CreateBookingView.as_view(),name='booking'),
    path('mydashboard/',OwnerDashboardView.as_view(),name='owner-dashboard'),
    path('search/',OwnerDashboardSearchView.as_view(),name='booking-search'),
    path('delete/',DeleteBooking,name='booking-delete'),
]