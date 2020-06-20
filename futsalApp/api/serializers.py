from rest_framework import serializers, permissions, authentication
from futsalApp.models import Futsal

class FutsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = [
            'id',
            'name',
            'location',
            'main_img',
            'cover_img',
            'description',
            'price',
            'timestamp',
        ]