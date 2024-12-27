from projects.models import Project, Notification
from .forms import ProjectForm


def global_notifications(request):
    if request.user.is_authenticated:
        # Fetch the latest 5 notifications and unread count for the logged-in user
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'global_notifications': notifications,
            'unread_notification_count': unread_count,
        }
    return {}