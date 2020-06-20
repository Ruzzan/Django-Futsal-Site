from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import *
from django.contrib.auth import authenticate

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email',]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    favourites = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['user','avatar', 'favourites', 'is_owner']
        depth = 1
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError('Password must match')
        return data
    
    def create(self, validate_data):
        user = User.objects.create(
            username = validate_data.get('username'),
            email    = validate_data.get('email')
        )
        user.set_password(validate_data.get('password'))
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    message = 'User Deactivated'
                    raise serializers.ValidationError(message)
            else:
                message = "Invalid Credentials"
                raise serializers.ValidationError(message)
        else:
            message = "Provide both username and password."
            raise serializers.ValidationError(message)
        return data

            

