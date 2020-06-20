from .serializers import FutsalSerializer
from rest_framework import generics, mixins, permissions, authentication
from futsalApp.models import Futsal
from django.db.models import Q

class FutsalListAPI(generics.ListAPIView):
    serializer_class = FutsalSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Futsal.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(locaton__icontains=query)
            )
        return qs
    
class FutsalDetailAPI(generics.RetrieveAPIView):
    serializer_class = FutsalSerializer
    queryset    = Futsal.objects.all()
    permissions = [permissions.AllowAny]

