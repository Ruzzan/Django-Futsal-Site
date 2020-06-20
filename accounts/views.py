from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from futsalApp.models import Futsal
from django.views import generic
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def RegisterView(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome {}'.format(username))
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

def logged_in_message(sender, user, request, **kwargs):
    user = request.user
    messages.info(request, 'Welcome {}'.format(user.username))
user_logged_in.connect(logged_in_message)

# update page of the user 
@login_required
def UpdateProfileView(request):
    user = request.user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST or None,request.FILES or None,instance = user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated')
            redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user':user,
    }
    return render(request, 'accounts/profile.html',context)
        
@login_required
def ChangePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is successfully changed.')
            return redirect('change-password')
        else:
            messages.error(request, 'Please enter correctly.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.html', {'form':form})


def AddToFavourite(request):
    print('liked')
    context = {}
    user = request.user
    futsal = get_object_or_404(Futsal, id=request.POST.get('futsal_id',None))
    print(futsal)
    is_saved = False
    if request.method == "POST":
        if user.profile.favourites.filter(id=futsal.id).exists():
            user.profile.favourites.remove(futsal)
            is_saved = False
        else:
            user.profile.favourites.add(futsal)
            is_saved = True
    context = {
        'is_saved':is_saved,
    }
    return JsonResponse({'data':context})


class UserDashboardView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'accounts/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_saved_futsals(self):
        user = self.request.user
        futsals = user.profile.favourites.all()
        return futsals

    

    def get_context_data(self, *args, **kwargs):
        booking = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)
        context['queryset'] = booking
        context['today_booking'] = booking.filter(date=datetime.datetime.today())
        context['saved'] = self.get_saved_futsals()
        return context
