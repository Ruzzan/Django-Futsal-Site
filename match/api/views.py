from .serializers import MatchSerializer, MatchObjectSerializer
from rest_framework import generics, mixins
from match.models import Match, MatchObject


class MatchListAPI(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = MatchSerializer

    def get_queryset(self):
        qs = Match.objects.all()
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class MatchDetailAPI(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = MatchSerializer
    queryset         = Match.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MatchObjectListAPI(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = MatchObjectSerializer

    def get_queryset(self):
        qs = MatchObject.objects.all()
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MatchObjectDetailAPI(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = MatchObjectSerializer
    queryset  = MatchObject.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



