from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (RegisterView, UpdateProfileView, ChangePasswordView,AddToFavourite,UserDashboardView)

urlpatterns = [
    path('signup/',RegisterView,name='signup'),
    path('profile/',UpdateProfileView,name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name="accounts/logout.html"),name='logout'),
    path('change-password/',ChangePasswordView,name='change-password'),
    path('save/',AddToFavourite,name='save'),
    path('dashboard/',UserDashboardView.as_view(),name='dashboard'),
]