"""Url configuration for ticket."""

from django.urls import path
from rest_framework.routers import SimpleRouter
from ticket.api.views import(
    TicketCreateView,
    TicketStatusListCreateView,
    TicketPriorityListCreateView
)

app_name = "ticket.api"

router = SimpleRouter()
urlpatterns = [
   path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('status/', TicketStatusListCreateView.as_view(), name='ticket-status-list-create'),
    path('priorities/', TicketPriorityListCreateView.as_view(), name='ticket-priority-list-create'),
]
