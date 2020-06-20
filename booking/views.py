from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import CreateBookingForm
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from futsalApp.models import Futsal
from django.db.models import Q
import datetime
from django.contrib import messages

class CreateBookingView(LoginRequiredMixin,generic.CreateView):
    model = Booking
    template_name = 'booking/create.html'
    form_class    = CreateBookingForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        while Booking.objects.filter(futsal=instance.futsal,date=instance.date,time=instance.time).exists():
            messages.error(self.request,'Already booked by other.')
            instance = form.save(commit=False)
            return redirect('booking')
        instance.save()
        messages.success(self.request, 'Booking done in {} for {} {}.'.format(
            instance.futsal,instance.date,instance.time
        ))
        return redirect('booking')
    
class OwnerDashboardView(LoginRequiredMixin,generic.ListView):
    model    = Booking
    template_name = 'booking/owner_dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(futsal__owner = self.request.user,futsal=self.get_futsal())

    def get_futsal(self):
        return Futsal.objects.get(owner = self.request.user)

    def get_valid_bookings(self):
        count = 0
        for i in self.get_queryset():
            if i.is_valid():
                count+=1
        return count

    def get_context_data(self, *args, **kwargs):
        booking = self.get_queryset()
        futsal  = self.get_futsal()
        context = super().get_context_data(*args, **kwargs)
        context['futsal'] = futsal
        context['queryset'] = booking
        context['today_booking'] = booking.filter(date=datetime.datetime.today())
        context['valid_booking'] = self.get_valid_bookings()
        return context


class OwnerDashboardSearchView(LoginRequiredMixin, generic.ListView):
    template_name = 'booking/search.html'
    model = Booking

    def get_futsal(self):
        return Futsal.objects.get(owner = self.request.user)

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        futsal       = self.get_futsal()
        bookings = Booking.objects.filter(
            fullname__icontains=search_query,
            futsal=futsal
        )
        return bookings
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('q')
        context['queryset'] = self.get_queryset()
        return context

def DeleteBooking(request):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=request.POST.get('booking_id'))
        if booking.futsal.owner == request.user:
            booking.delete()
            messages.success(request, 'Booking Deleted')
    return redirect('owner-dashboard')


