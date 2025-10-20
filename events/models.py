from django.db import models
from django.conf import settings

# Create your models here.
# event model
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True) #verbose_name='End Time') #required for google calender api
    category = models.CharField(max_length=100)
    # foreign key to the organizer
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events_organized'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
# comment model (student can comment on events they like)
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# like model 
class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'event')
