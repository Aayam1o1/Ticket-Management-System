from rest_framework import serializers
from menu.models import Menu
from account.models import Role

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