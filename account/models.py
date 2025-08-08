"""Models for the user management."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from account.validators import validate_phone_number


class ValidPhoneNumberField(PhoneNumberField):

    """Class to validate phone number."""

    default_validators = [validate_phone_number]


class CustomUserManager(BaseUserManager):
    
    """Custom manager for the User model to handle user creation."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")
        if not password:
            raise ValueError("The password field must be set")

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


        
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField('Permission', blank=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    phone_number = ValidPhoneNumberField(_("Phone Number"))
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    objects = CustomUserManager()

    def clean(self):
        """Validate to ensure phone_number."""
        if not self.phone_number:
            raise ValidationError("Phone number must be provided.")
        

class Permission(models.Model):
    permission_type = models.CharField(max_length=50, unique=True) 
    description = models.TextField(blank=True)

    def __str__(self):
        return self.permission_type
