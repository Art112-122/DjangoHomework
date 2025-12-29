from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(
        User,
        related_name="topics",
        blank=True,
    )

    def __str__(self):
        return self.name


class TopicActivity(models.Model):
    ACTION_CHOICES = (
        ("created", "Created"),
        ("deleted", "Deleted"),
        ("updated", "Updated"),
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.action}"
