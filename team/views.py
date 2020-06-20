from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .forms import TeamForm
from .models import Team, TeamMember
from match.models import Match,MatchObject
from django.views import generic
from django.contrib import messages
from django.db.models import Q

class TeamIndexView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = 'team/index.html'
    context_object_name = 'teams'

    def get_queryset(self):
        queryset = Team.objects.all().exclude(members__id=self.request.user.id).order_by('?')[:4]
        return queryset

    def get_team(self):
        try:
            member = TeamMember.objects.get(user=self.request.user)
            return member.team
        except:
            member = None
        return None

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_team'] = self.get_team()
        return context
    

class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Create Team'
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.admin = self.request.user
        instance.save()
        instance.members.add(self.request.user)
        messages.success(self.request, 'Team created successfully.')
        return redirect(instance.get_absolute_url())

class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = 'team/team.html'
    context_object_name = 'team'
    slug_url_kwarg = 'slug'

    def get_team(self):
        team = get_object_or_404(Team, slug=self.kwargs.get('slug'))
        return team

    def get_match_requests(self):
        try:
            match_requests = Match.objects.filter(matchobject__opponent=None)
        except:
            match_requests = None
        return match_requests
    
    def get_matches(self):
        try:
            matches = MatchObject.objects.filter(
            Q(match = self.get_match_requests()[:1]) |
            Q(opponent = self.get_team())
            )
        except:
            matches = None
        return matches

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['match_requests'] = self.get_match_requests()
        context['matches'] = self.get_matches()
        return context
    
class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    template_name = 'team/edit.html'
    form_class    = TeamForm

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Edit Team'
        return context

    def get_queryset(self):
        return Team.objects.filter(admin=self.request.user)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.admin = self.request.user
        instance.slug  = instance._get_unique_slug()
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = 'team/delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'team'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Team deleted successfully.')
        return super().delete(self,request, *args, **kwargs)

class JoinTeamView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('team-detail',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        team   = get_object_or_404(Team, slug=self.kwargs.get('slug'))
        already_member = TeamMember.objects.filter(user=self.request.user).exists()
        if already_member:
            messages.warning(self.request, 'Already in another team.')
            return HttpResponseRedirect(self.get_redirect_url())
        try:
            TeamMember.objects.create(user=self.request.user,team=team)
        except:
            messages.warning(self.request, 'Already in team.')
        else:
            messages.success(self.request, 'You are now a member.')
        
        return super().get(request, *args, **kwargs)


class LeaveTeamView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('team-detail', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        try:
            membership = TeamMember.objects.filter(
            user = self.request.user,
            team__slug = self.kwargs.get('slug')
        ).get()
        except TeamMember.DoesNotExists:
            messages.warning(self.request, 'Sorry you are not in the team.')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the team.')

        return super().get(request, *args, **kwargs)

class RemoveMemberView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('team-detail', kwargs={'slug':self.kwargs.get('slug')})

    def post(self, request, *args, **kwargs):
        try:
            member = TeamMember.objects.get(user__id = self.request.POST.get('member_id'))
        except:
            messages.warning(self.request, 'Error')
        else:
            member.delete()
            messages.success(self.request, 'Removed')
        return self.get(request, *args, **kwargs)

class TeamSearchView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = 'team/search.html'
    context_object_name = 'teams'

    def get_queryset(self):
        search_query = []
        search_term = self.request.GET.get('q')
        if search_term is not None:
            search_query = Team.objects.filter(
                Q(name__icontains = search_term)
            )
        return search_query
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['teams'] = self.get_queryset()
        context['search_term'] = self.request.GET.get('q')
        return context
