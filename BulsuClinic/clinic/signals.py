from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib.auth.signals import user_logged_in
from clinic.models import CustomUser

@receiver(user_logged_in)
def set_current_project(sender, request, user, **kwargs):
    if user.is_superuser:
       return redirect('manage_staff')
    else:
       return redirect('dashboard')


