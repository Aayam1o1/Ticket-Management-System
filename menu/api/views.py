# views.py
from rest_framework import generics
from menu.models import Menu
from menu.api.serializers import (
    MenuCreateSerializer,
    RecursiveMenuSerializer
)
from rest_framework.permissions import IsAuthenticated


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.filter(parent__isnull=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuCreateSerializer
        return RecursiveMenuSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MenuCreateSerializer
        return RecursiveMenuSerializer

    def perform_update(self, serializer):
        serializer.save()  