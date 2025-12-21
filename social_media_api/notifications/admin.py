from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ['recipient', 'actor', 'verb', 'timestamp', 'read']
    list_filter = ['read', 'timestamp']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
