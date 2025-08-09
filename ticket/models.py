from django.db import models
from django.contrib.auth import get_user_model
from menu.models import Menu
User = get_user_model()


class Ticket(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu,  related_name="menu_tickets")

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey('TicketStatus', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey('TicketPriority', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class TicketStatus(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class TicketPriority(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name