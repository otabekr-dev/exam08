from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Events(models.Model):
    class Event_Type(models.TextChoices):
        ONLINE = 'ONLINE', 'Online'
        OFFLINE = 'OFFLINE', 'Offline'

    title = models.CharField(max_length=60)
    description = models.TextField()
    event_type = models.CharField(
        max_length=25,
        choices=Event_Type.choices
    )
    location = models.CharField(max_length=128, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    

    def __str__(self):
        return f'{self.id}|{self.title}'
    