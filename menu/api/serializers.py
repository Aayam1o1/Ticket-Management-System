from rest_framework import serializers
from menu.models import Menu
from account.models import Role
from django.contrib.auth import get_user_model

User = get_user_model()

class MenuCreateSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Role.objects.all(), required=True
    )
    class Meta:
        model = Menu
        fields = ['id', 'name', 'parent', 'roles']
        
        
class RecursiveMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return RecursiveMenuSerializer(obj.children.all(), many=True).data
        return []
    

class UserMenuAssignSerializer(serializers.ModelSerializer):
    assigned_menus = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Menu.objects.all(),
        write_only=True
    )
    assigned_menus_details = RecursiveMenuSerializer(
        source='assigned_menus',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'assigned_menus', 'assigned_menus_details']