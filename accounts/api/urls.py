from django.urls import path
from .views import RegisterAPIView,ProfileAPIView, ProfileRetriveAPI,LoginView,LogoutView

urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('profile/',ProfileAPIView.as_view(),name='user-list-api'),
    path('profile/<int:pk>/',ProfileRetriveAPI.as_view(),name='user-api'),
    path('login/',LoginView.as_view(),name='api-login'),
    path('logout/',LogoutView.as_view(),name='api-logout'),
]