from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .paginator import proper_paginator
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .models import Futsal
from .forms import FutsalUpdateForm
from accounts.models import Profile
from booking.models import Booking
from booking.forms import BookingForm, CreateBookingForm
import datetime
from django.db.models import Q
from team.models import Team, TeamMember

class HomePageView(LoginRequiredMixin,generic.ListView):
    model = Futsal
    template_name = 'futsalApp/index.html'
    queryset = Futsal.objects.all().order_by('?')[:3]
    context_object_name = 'futsals'

    def get_team(self):
        try:
            member = TeamMember.objects.get(user=self.request.user)
            return member.team.slug
        except:
            member = None
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['owner_futsals'] = Futsal.objects.filter(owner = self.request.user)
        context['team'] = self.get_team()
        return context
           
def FutsalListView(request):
    futsal_list = Futsal.objects.all().order_by('-id')
    paginator   = Paginator(futsal_list, 4)
    page        = request.GET.get('page')

    try:
        futsals = paginator.page(page)
    except PageNotAnInteger:
        futsals = paginator.page(1)
    except EmptyPage:
        futsals = paginator.page(paginator.num_pages)
    
    # To show limited number of paginators 
    if page is None:
        start_index = 0
        end_index   = 7
    else:
        (start_index, end_index) = proper_paginator(futsals, index=4)
    
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'futsals':futsals,
        'page_range':page_range,
    }
    return render(request, 'futsalApp/list.html', context)

    

class FutsalUpdateView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):
    model = Futsal
    form_class = FutsalUpdateForm
    success_message = 'Futsal Edited Successfully.'
    template_name = 'futsalApp/edit.html'

    def get_queryset(self):
        return Futsal.objects.filter(owner = self.request.user)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.slug  = instance._get_unique_slug()
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

def FutsalSearchView(request):
    search_result = []
    if request.GET.get('futsal_name'):
        futsal = request.GET['futsal_name']
        search_result = Futsal.objects.filter(Q(name__icontains=futsal))
    
    if request.GET.get('futsal_location'):
        location = request.GET['futsal_location']
        search_result = Futsal.objects.filter(Q(location__icontains=location))
    
    if request.GET.get('futsal_price'):
        price = request.GET['futsal_price']
        search_result = Futsal.objects.filter(Q(price__lte=price))
    
    paginator = Paginator(search_result, 6)
    page      = request.GET.get('page')

    try:
        futsals = paginator.page(page)
    except PageNotAnInteger:
        futsals = paginator.page(1)
    except EmptyPage:
        futsals = paginator.page(paginator.num_pages)
        
    # To show limited number of paginators 
    if page is None:
        start_index = 0
        end_index   = 7
    else:
        (start_index, end_index) = proper_paginator(futsals, index=4)
    
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'futsals':futsals,
        'page_range':page_range,
    }

    return render(request, 'futsalApp/search.html', context)



def FutsalDetailView(request, slug):
    futsal = get_object_or_404(Futsal, slug=slug)
    user  = request.user
    # Booking form 
    if request.method == "POST":
        form = BookingForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user 
            instance.futsal = futsal
            pre_booked = Booking.objects.filter(futsal=instance.futsal,date=instance.date,time=instance.time).exists()
            # check if futsal is pre booked 
            if pre_booked:
                messages.error(request,'Already booked by others.')
                instance = form.save(commit=False)
                return HttpResponseRedirect(futsal.get_absolute_url())

            instance.save()
            messages.success(request, 'Futsal Game Booked Successfully.')
            return HttpResponseRedirect(futsal.get_absolute_url())   
    else:
        print('error')
        form = BookingForm()
    # check if saved:
    is_saved = False
    if user.profile.favourites.filter(id=futsal.id).exists():
        is_saved = True
    else:
        is_saved = False
    
    # show bookings of the futsal for today
    bookings = Booking.objects.filter(
        futsal=futsal,
        date=datetime.date.today(),
        )

    context = {
        'form':form,
        'bookings':bookings,
        'futsal':futsal,
        'today':datetime.date.today(),
        'is_saved':is_saved,
        'lat':futsal.lat,
        'lng':futsal.lng,
    }
    return render(request, 'futsalApp/detail.html', context)
           
# def comment(request):
#     context = {}
#     if request.method == "POST":
#         form = ReviewForm(request.POST or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.futsal = request.POST.get('futsal_id')
#             print(instance.futsal)
#             instance.user = request.user
#             instance.save()
#             context['comment'] = instance.review
#             context['user']    = request.user.username
#             context['date']    = instance.date
#             context['futsal']  = instance.futsal
#             return JsonResponse({'data':context})
#     else:
#         form = ReviewForm()
#     return JsonResponse({'error':'Error occoured.'})


# class FutsalDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
#     model = Futsal
#     template_name = 'futsalApp/detail.html'
#     context_object_name = 'futsal'
#     slug_url_kwarg = 'slug'
#     form_class = BookingForm

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset=queryset)
#         return obj

#     def check_if_saved(self):
#         user = self.request.user
#         is_saved = False
#         if user.profile.favourites.filter(id=self.get_object().id).exists():
#             is_saved = True
#         return is_saved

#     def get_success_url(self):
#         return HttpResponseRedirect(reverse('futsal-detail', kwargs={'slug':self.get_object().slug}))
    
#     def get_context_data(self, **kwargs):
#         context = super(FutsalDetailView, self).get_context_data(**kwargs)
#         context['form'] = BookingForm(initial={'post':self.get_object()})
#         context['bookings'] = Booking.objects.filter(
#             futsal=self.get_object(),
#             date=datetime.date.today(),
#             )
#         context['today'] = datetime.date.today()
#         context['is_saved'] = self.check_if_saved()
#         context['review_form'] = ReviewForm()
#         # for frontend values
#         context['lat'] = self.get_object().lat
#         context['lng'] = self.get_object().lng
#         return context
    
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = self.request.user
#             instance.futsal = self.get_object()
#             while Booking.objects.filter(futsal=instance.futsal,date=instance.date,time=instance.time).exists():
#                 messages.error(self.request,'Already booked')
#                 instance.save(commit=False)
#                 return HttpResponseRedirect(self.get_object().get_absolute_url())
#             instance.save()
#             messages.success(self.request, 'Futsal Game Booked Successfully.')
#             return self.get_success_url()
#         else:
#             messages.error(self.request, 'Booking Failed')
#             return HttpResponseRedirect(self.get_object().get_absolute_url())