from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -----------------------------------
# UserProfile Model
# -----------------------------------
class UserProfile(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    # Optional: add timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    # Optional: helper methods for role checks
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_librarian(self):
        return self.role == self.ROLE_LIBRARIAN

    def is_member(self):
        return self.role == self.ROLE_MEMBER


# -----------------------------------
# Signals to Create / Save UserProfile
# -----------------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Ensure UserProfile is saved whenever the User is saved.
    """
    # Use hasattr check to avoid errors if profile doesn't exist
    if hasattr(instance, 'profile'):
        instance.profile.save()
