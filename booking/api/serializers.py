from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Booking
        fields = [
            'id',
            'fullname',
            'phone',
            'user',
            'futsal',
            'time',
            'date',
            'timestamp',
        ]
        read_only_fields = ['user',]

