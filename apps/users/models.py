from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("researcher", "Researcher"),
        ("student", "Student"),
        ("freelancer", "Freelancer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="researcher"
    )

    is_subscribed = models.BooleanField(default=True)
