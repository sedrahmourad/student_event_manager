from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomeUser(AbstractUser):
    # add extra fields
    pass

#student profile linked to custom user

class student(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE, related_name="student_profile")
    grade = models.CharField(max_length=50, blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"student: {self.user.username}"

# Organizer profile linked to CustomUser
class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="organizer_profile")
    organization_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True, null=True)  # e.g., Event Manager, Coordinator

    def __str__(self):
        return f"Organizer: {self.user.username}"
