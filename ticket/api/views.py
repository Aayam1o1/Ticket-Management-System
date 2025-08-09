from rest_framework import generics
from ticket.models import (
    Ticket,
    TicketStatus,
    TicketPriority
)
from ticket.api.serializers import (
    TicketSerializer,
    TicketStatusSerializer,
    TicketPrioritySerializer
)
from rest_framework.permissions import IsAuthenticated
from account.permissions import CanCreateTicket


class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanCreateTicket]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
class TicketStatusListCreateView(generics.ListCreateAPIView):
    queryset = TicketStatus.objects.all().order_by('-weight')
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated]


class TicketPriorityListCreateView(generics.ListCreateAPIView):
    queryset = TicketPriority.objects.all().order_by('-weight')
    serializer_class = TicketPrioritySerializer
    permission_classes = [IsAuthenticated]
        
        
        