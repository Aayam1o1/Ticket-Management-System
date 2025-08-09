from django.contrib import admin
from menu.models import Menu

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'created_by', 'created_at')
    list_filter = ('created_at', 'roles')
    search_fields = ('name',)
    filter_horizontal = ('roles',)
    autocomplete_fields = ('parent', 'created_by')
    ordering = ('-created_at',)

admin.site.register(Menu, MenuAdmin)