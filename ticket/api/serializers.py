from rest_framework import serializers
from ticket.models import (
    Ticket,
    TicketPriority,
    TicketStatus
)
from menu.models import Menu

class TicketSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Menu.objects.all()
    )

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'priority', 'menu', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ['id', 'name', 'weight']


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = ['id', 'name', 'weight']