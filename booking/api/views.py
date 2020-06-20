from .serializers import BookingSerializer
from booking.models import Booking
from rest_framework import generics, mixins,permissions

class BookingListAPI(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = Booking.objects.all()
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class BookingDetailAPI(generics.RetrieveAPIView,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = BookingSerializer
    queryset         = Booking.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)