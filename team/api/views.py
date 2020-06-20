from .serializers import TeamSerializer, TeamMemberSerializer
from team.models import Team, TeamMember
from rest_framework import generics, mixins, permissions, authentication

class TeamListAPI(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = TeamSerializer

    def get_queryset(self):
        qs = Team.objects.all()
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(admin=self.request.user)

class TeamDetailAPI(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = TeamSerializer
    queryset         = Team.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TeamMemberListAPI(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = TeamMemberSerializer
    def get_queryset(self):
        qs = TeamMember.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class TeamMemberDetailAPI(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = TeamMemberSerializer
    queryset         = TeamMember.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
