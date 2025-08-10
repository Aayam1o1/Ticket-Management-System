"""Url configuration for ticket."""

from django.urls import path
from rest_framework.routers import SimpleRouter
from ticket.api.views import(
    TicketCreateView,
    TicketStatusListCreateView,
    TicketPriorityListCreateView,
    TicketListView,
    TicketStatusListView,
    TicketUpdateView,
    TicketAssignView
    
)

app_name = "ticket.api"

router = SimpleRouter()
urlpatterns = [
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('status/', TicketStatusListCreateView.as_view(), name='ticket-status-list-create'),
    path('priorities/', TicketPriorityListCreateView.as_view(), name='ticket-priority-list-create'),
    path('list/', TicketListView.as_view(), name='ticket-list'), 
    path('status/list/', TicketStatusListView.as_view(), name='ticket-status-list'),  
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
]
