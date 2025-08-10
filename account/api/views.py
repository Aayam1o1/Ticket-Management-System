from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from account.models import (
    User,
    Role,
    Permission,
)
from account.api.serializers import (
    RegisterSerializer,
    RoleSerializer,
    PermissionSerializer,
    CustomTokenObtainPairSerializer,
    AssignPermissionSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from account.permissions import CanManageRoles, CanManagePermissions

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class RoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CanManageRoles]

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CanManageRoles]
    

class PermissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [CanManagePermissions] 

class PermissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [CanManagePermissions]
    

class RolePermissionListAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = PermissionSerializer 
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        role = self.get_object()
        permissions = role.permissions.all()
        serializer = self.get_serializer(permissions, many=True)
        return Response(serializer.data)


class AssignPermissionsToRoleAPIView(generics.CreateAPIView):
    serializer_class = AssignPermissionSerializer
    def post(self, request, *args, **kwargs):
        serializer = AssignPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Permissions assigned to role."}, status=status.HTTP_200_OK)
