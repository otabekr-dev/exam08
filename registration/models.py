from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from events.models import Events

class Registration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_registrations"  
    )
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        related_name="registrations"         
    )
    registered_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.id}| {self.user} → {self.event}"