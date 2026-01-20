from django.conf import settings
from django.db import models

class PaymentEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    raw = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.event_type} ({self.stripe_event_id})"
