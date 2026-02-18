from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Interactive Research State
    research_topic = models.CharField(max_length=255, null=True, blank=True)
    current_hypothesis = models.TextField(null=True, blank=True)
    research_stage = models.CharField(
        max_length=50,
        default="exploration"
    )

    def __str__(self):
        return f"Session {self.id} - {self.user.username}"


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20)  # user / agent
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ResearchMemory(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="memories")
    key = models.CharField(max_length=100)
    value = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.key} - Session {self.session.id}"
