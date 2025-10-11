from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

# define user roles
class UserRole(models.TextChoices):
    STUDENT = 'student', _('Student')
    ORGANIZER = 'organizer', _('Organizer')

# custom user model extending abstract user
class CustomUser(AbstractUser):
    # role field 
    role = models.CharField(
        max_length=100,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        verbose_name='Role'
    )
    # student specific field (major)
    major = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Major/Interest Area'
    )
    # organizer specific field 
    organization_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Organization Name'
    )
    name = models.CharField(max_length=200, verbose_name='Full Name')
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

