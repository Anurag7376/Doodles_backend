from django.db import models
from django.conf import settings

class Subscription(models.Model):
    PLAN_CHOICES = (
        ("free", "Free"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
