from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_profile_picture(file):
    max_size = 2 * 1024 * 1024
    valid_extensions = ['.jpg', '.jpeg', '.png']

    if file.size > max_size:
        raise ValidationError('Profile picture file size cannot exceed 2 MB.')
    if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError('Invalid file format. Please upload a JPG, JPEG, or PNG file.')


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        validators=[validate_profile_picture]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('nurse', 'Nurse'),
        ('dentist', 'Dentist'),
        ('physician', 'Physician'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.role}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.user.email
    
