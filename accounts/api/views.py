from rest_framework import generics, parsers, mixins
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from django.contrib.auth.models import User
from accounts.models import Profile
from .serializers import UserRegisterSerializer, ProfileSerializer, LoginSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser,parsers.FormParser,parsers.JSONParser]

class ProfileAPIView(generics.ListAPIView,mixins.CreateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(user=request.user)

class ProfileRetriveAPI(generics.RetrieveAPIView,mixins.UpdateModelMixin):
    serializer_class = ProfileSerializer
    queryset         = Profile.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user  = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key}, status=200)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        logout(request)
        return Response({'message':'Logged Out'}, status=200)
        



