from rest_framework import serializers
from ticket.models import (
    Ticket,
    TicketPriority,
    TicketStatus
)
from menu.models import Menu
from django.contrib.auth import get_user_model
from ticket.utils import get_ancestors
User = get_user_model()


class SimpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name']




class TicketSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Menu.objects.all(), write_only=True
    )
    menu_details = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'menu', 'menu_details', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']

    def get_menu_details(self, obj):
        assigned_menus = obj.menu.all()
        all_menus = set()

        for menu in assigned_menus:
            all_menus.add(menu)
            # Use your helper function instead of non-existent method
            ancestors = get_ancestors(menu)[1:]  # exclude self
            for ancestor in ancestors:
                if ancestor in assigned_menus:
                    all_menus.add(ancestor)

        serializer = SimpleMenuSerializer(all_menus, many=True)
        return serializer.data

    def validate_menu(self, menus):
        user = self.context['request'].user
        # Admin/Supervisor can create ticket with any menu
        if user.role and user.role.name in ['Admin', 'Supervisor']:
            return menus

        # Otherwise user must have assigned menus matching all chosen
        if not user.assigned_menus.exists():
            raise serializers.ValidationError("You have no assigned menus, so you cannot create tickets.")

        for m in menus:
            if not user.assigned_menus.filter(id=m.id).exists():
                raise serializers.ValidationError(
                    f"You cannot create tickets with menu '{m.name}'."
                )
        return menus
    
class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ['id', 'name', 'weight']


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = ['id', 'name', 'weight']
        

class TicketAssignSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    menu = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Menu.objects.all(), required=False
    )
    
    class Meta:
        model = Ticket
        fields = ['assigned_to', 'menu']

