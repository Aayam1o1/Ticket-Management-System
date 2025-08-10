from django.db import models
from django.contrib.auth import get_user_model
from account.models import Role

User = get_user_model()

class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    roles = models.ManyToManyField(Role, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name

    def get_descendants(self):
        """Recursively fetch all descendants of this menu item."""
        descendants = set(self.children.all())
        for child in self.children.all():
            descendants.update(child.get_descendants())
        return descendants