from rest_framework import generics
from ticket.models import (
    Ticket,
    TicketStatus,
    TicketPriority
)
from ticket.api.serializers import (
    TicketSerializer,
    TicketStatusSerializer,
    TicketPrioritySerializer,
    TicketAssignSerializer
)
from rest_framework.permissions import IsAuthenticated
from account.permissions import (
    CanCreateTicket,
    CanManageStatus,
    CanManagePriority,
    CanViewTicket,
    CanEditTicket
)
from rest_framework.exceptions import PermissionDenied
from ticket.utils import get_descendants

class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanCreateTicket]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role and user.role.name not in ['Admin', 'Supervisor']:
            if not user.assigned_menus.exists():
                raise PermissionDenied("You have no assigned menus and cannot create tickets.")
        serializer.save(created_by=user)


class TicketStatusListCreateView(generics.ListCreateAPIView):
    """Manage statuses — requires permission."""
    queryset = TicketStatus.objects.all().order_by('-weight')
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated, CanManageStatus]


class TicketPriorityListCreateView(generics.ListCreateAPIView):
    """Manage priorities — requires permission."""
    queryset = TicketPriority.objects.all().order_by('-weight')
    serializer_class = TicketPrioritySerializer
    permission_classes = [IsAuthenticated, CanManagePriority]
    
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanViewTicket]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "assigned_menus") or not user.assigned_menus.exists():
            return Ticket.objects.none()

        assigned_menus = set()

        for menu in user.assigned_menus.all():
            # If menu has children, add itself and all descendants
            if menu.children.exists():
                assigned_menus.add(menu)
                assigned_menus.update(get_descendants(menu))
            else:
                assigned_menus.add(menu)

        return Ticket.objects.filter(menu__in=assigned_menus).distinct()



class TicketStatusListView(generics.ListAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated, CanManageStatus]

    def get_queryset(self):
        return TicketStatus.objects.all().order_by('-weight')
    
class TicketUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanEditTicket]

    def perform_update(self, serializer):
        user = self.request.user
        
        if user.role and user.role.name not in ['Admin', 'Supervisor']:
            if not serializer.instance.menu.filter(id__in=user.assigned_menus.values_list('id', flat=True)).exists():
                raise PermissionDenied("You don't have permission to update this ticket.")
        
        serializer.save()
        
        
class TicketAssignView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketAssignSerializer
    permission_classes = [IsAuthenticated, CanCreateTicket]  

    def perform_update(self, serializer):
        user = self.request.user
        ticket = self.get_object()

        # Only allow Admin/Supervisor to assign/reassign
        if user.role and user.role.name not in ['Admin', 'Supervisor']:
            raise PermissionDenied("Only Admin or Supervisor can assign/reassign tickets.")

        new_assigned_user = serializer.validated_data.get('assigned_to')

        # Check if it's already assigned to the same user
        if new_assigned_user and ticket.assigned_to == new_assigned_user:
            raise PermissionDenied("This ticket is already assigned to that user.")

        serializer.save()
        
        