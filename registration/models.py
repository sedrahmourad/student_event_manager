from django.db import models
from django.conf import settings

# Create your models here.
class Registration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Student'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Event'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')
    class Meta:
        # prevents user from registering for the same event twice
        unique_together = ('user', 'event')
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        # latest registration first
        ordering = ['-timestamp']
    def __str__(self):
        return f"{self.user.name} registered for {self.event.title}"
    

