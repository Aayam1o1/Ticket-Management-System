from rest_framework import serializers
from account.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    """Serailzer for registration of user."""
    
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'password1']

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