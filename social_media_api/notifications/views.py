from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    API endpoint for viewing user notifications.
    GET: List all notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return notifications for the current user."""
        return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationAsReadView(APIView):
    """
    API endpoint for marking a notification as read.
    POST: Mark a specific notification as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.read = True
        notification.save()

        return Response(
            {
                'message': 'Notification marked as read',
                'notification': NotificationSerializer(notification).data
            },
            status=status.HTTP_200_OK
        )
