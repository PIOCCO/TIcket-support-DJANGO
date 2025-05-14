from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, CustomPermission, User, Ticket, TicketLog, Issue
from django.utils.safestring import mark_safe


# Role Admin
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Permission Admin
@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('roles', 'permissions'),
        }),
    )
    filter_horizontal = ('roles', 'permissions')
    list_display = ('username', 'email', 'is_staff', 'is_superuser')

    
# Ticket Admin
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'category', 'created_by', 'assigned_to', 'created_at', 'ticket_picture')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('created_by', 'assigned_to')
    date_hierarchy = 'created_at'


# TicketLog Admin
@admin.register(TicketLog)
class TicketLogAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'created_by', 'action', 'created_at')
    search_fields = ('ticket__title', 'created_by__username', 'action')
    date_hierarchy = 'created_at'


