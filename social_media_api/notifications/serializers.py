from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    Displays notification details with actor information.
    """
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    timestamp_display = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'actor',
            'actor_username',
            'verb',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'timestamp_display',
            'read'
        ]
        read_only_fields = ['id', 'actor', 'timestamp']

    def get_timestamp_display(self, obj):
        """Return human-readable timestamp."""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.timestamp

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
