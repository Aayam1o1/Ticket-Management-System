from rest_framework import serializers
from account.models import (
    User,
    Role,
    Permission,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    """Serailzer for registration of user."""
    
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, label="Confirm password")
    role = serializers.PrimaryKeyRelatedField(
            queryset=Role.objects.all(),
            required=True
        )
    class Meta:
        model = User
        fields = ['id',
                'username',
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'password',
                'password1',
                'role'
            ]

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password1')
        return User.objects.create_user(**validated_data)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to allow login with username or email or phone."""

    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        return data
    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'permission_type', 'description']


class AssignPermissionSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        role_id = attrs.get('role_id')
        permission_ids = attrs.get('permission_ids')

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role not found.")

        permissions = Permission.objects.filter(id__in=permission_ids)
        if permissions.count() != len(permission_ids):
            raise serializers.ValidationError("Some permissions do not exist.")

        attrs['role'] = role
        attrs['permissions'] = permissions
        return attrs

    def create(self, validated_data):
        role = validated_data['role']
        permissions = validated_data['permissions']
        role.permissions.set(permissions)
        return role