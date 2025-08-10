# views.py
from rest_framework import generics
from menu.models import Menu
from menu.api.serializers import (
    MenuCreateSerializer,
    RecursiveMenuSerializer
)
from rest_framework.permissions import IsAuthenticated
from menu.api.serializers import UserMenuAssignSerializer
from django.contrib.auth import get_user_model
from account.permissions import (
    IsAdminOrSupervisor,
    IsSelfOrAdminSupervisor,
    CanManageMenu,
    
)

User = get_user_model()



class MenuListCreateView(generics.ListCreateAPIView):
    """Admins/Supervisors can list and create top-level menus."""
    permission_classes = [IsAuthenticated, CanManageMenu]

    def get_serializer_class(self):
        return MenuCreateSerializer if self.request.method == 'POST' else RecursiveMenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Admins/Supervisors can edit or delete menus."""
    permission_classes = [IsAuthenticated, CanManageMenu]
    lookup_field = 'id'

    def get_serializer_class(self):
        return MenuCreateSerializer if self.request.method in ['PUT', 'PATCH'] else RecursiveMenuSerializer

    def get_queryset(self):
        return Menu.objects.all()

    def perform_update(self, serializer):
        serializer.save()


class UserMenuAssignUpdateView(generics.UpdateAPIView):
    """Assign menus to a specific user (Admin/Supervisor only)."""
    queryset = User.objects.all()
    serializer_class = UserMenuAssignSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSupervisor]
    lookup_field = 'id'

    def perform_update(self, serializer):
        selected_menus = serializer.validated_data.get('assigned_menus', [])

        all_menus_to_assign = set()
        visited = set()
        for menu in selected_menus:
            if menu.id not in visited:
                visited.add(menu.id)
                all_menus_to_assign.add(menu)
                all_menus_to_assign.update(self.get_all_descendants(menu, visited))

        serializer.save(assigned_menus=list(all_menus_to_assign))

    def get_all_descendants(self, menu, visited):
        descendants = set()
        for child in menu.children.all():
            if child.id not in visited:
                visited.add(child.id)
                descendants.add(child)
                descendants.update(self.get_all_descendants(child, visited))
        return descendants

class UserAssignedMenusRetrieveView(generics.RetrieveAPIView):
    """View assigned menus for a specific user."""
    queryset = User.objects.all()
    serializer_class = UserMenuAssignSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdminSupervisor]
    lookup_field = 'id'

