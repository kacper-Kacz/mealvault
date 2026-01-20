from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"
