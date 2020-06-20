from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from team.models import Team, TeamMember
from booking.models import Booking
from .models import Match, MatchObject
from .forms import MatchForm
import datetime
from django.db.models import Q

class MatchIndexView(LoginRequiredMixin, generic.ListView):
    model = Match
    template_name = 'match/index.html'

    def get_queryset(self):
        # this returns only the match requests who has no match objects
        match_requests = Match.objects.filter(matchobject__opponent=None)
        print(match_requests)
        return match_requests

    def check_team(self):
        try:
            has_team = TeamMember.objects.filter(user=self.request.user).exists()
        except:
            has_team = False
        return has_team

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['match_requests'] = self.get_queryset()
        context['has_team'] = self.check_team()
        return context

class CreateMatchView(LoginRequiredMixin, generic.CreateView):
    model = Match
    template_name = 'match/create.html'
    form_class = MatchForm

    def get_team(self):
        try:
            team = TeamMember.objects.get(user=self.request.user).team
            return team
        except:
            team = None
        return team

    def check_booking(self, obj):
        booking = Booking.objects.filter(futsal=obj.futsal,date=obj.date,time=obj.start_time).exists()
        return booking
    
    def check_match(self, obj):
        match = Match.objects.filter(futsal=obj.futsal,date=obj.date,start_time=obj.start_time).exists()
        return match

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.team = self.get_team()
        check_booking = self.check_booking(obj=instance)
        check_match   = self.check_match(obj=instance)
        while check_booking or check_match:
            instance = form.save(commit=False)
            messages.error(self.request,'Already booked for {} {}\n Try Again'.format(
                instance.date, instance.start_time))
            return redirect('match-create')
        # if there is no other bookings save !
        instance.save()
        messages.success(self.request, 'Match Request Sent.')
        return HttpResponseRedirect(instance.team.get_absolute_url())


class MatchFixView(LoginRequiredMixin, generic.RedirectView):
    
    def get_team(self): # users team 
        try:
            team = TeamMember.objects.get(user=self.request.user)
        except:
            team = None
        return team

    def get_redirect_url(self, *args, **kwargs):
        _team = self.get_team()
        team  = _team.team # users team 
        return reverse('team-detail', kwargs={'slug':team.slug})

    def post(self, request, *args, **kwargs):
        match_id = self.request.POST.get('match_id')
        team     = self.get_team() # users team 
        o_team   = self.request.POST.get('team_id') # opponent team
        print(o_team)
        try:
            match = Match.objects.get(id=match_id) # current match id to be post
            # new match object (team = team from list + opponent = users team )
            fix_match = MatchObject.objects.create(match=match, opponent=team.team)
            fix_match.save()
            messages.success(self.request, 'Game Fixed Successfully')
        except Exception as e:
            print(e)
            messages.warning(self.request, 'An error occoured')
        return super().get(request, *args, **kwargs)



class MatchSearchView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = 'match/search.html'
    context_object_name = 'matches'

    def get_queryset(self):
        search_query = []
        request = self.request
        if request.GET.get('search_query'):
            search_term = request.GET['search_query']
            search_query = Match.objects.filter(
                Q(team__name__icontains = search_term) |
                Q(futsal__name__icontains = search_query)
            )
        
        if request.GET.get('game_type'):
            game = request.GET['game_type'] 
            search_query = Match.objects.filter(
                Q(game_type = game)
            )
        return search_query
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['match_requests'] = self.get_queryset()
        return context
