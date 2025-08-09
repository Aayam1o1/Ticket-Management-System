from django.contrib import admin
from ticket.models import (
    Ticket,
    TicketPriority,
    TicketStatus
)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_menus', 'status', 'priority', 'created_by', 'created_at')
    list_filter = ('status', 'priority', 'menu', 'created_at')  
    search_fields = ('title', 'description')
    autocomplete_fields = ('menu', 'status', 'priority', 'created_by') 
    ordering = ('-created_at',)

    def get_menus(self, obj):
        return ", ".join(menu.name for menu in obj.menu.all())
    get_menus.short_description = "Menus"


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')
    ordering = ('-weight',)
    search_fields = ('name',)


@admin.register(TicketPriority)
class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')
    ordering = ('-weight',)
    search_fields = ('name',)
