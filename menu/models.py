from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model

class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name

    def level(self):
        """
        Return the level of the menu:
        Level 1: No parent
        Level 2: Has parent but parent has no parent
        Level 3: Has parent, and parent has parent
        """
        if not self.parent:
            return 1
        elif self.parent and not self.parent.parent:
            return 2
        elif self.parent and self.parent.parent:
            return 3
        return 0