from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from account.models import User
from account.api.serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from account.api.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer