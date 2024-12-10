from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'To do'),
        ('DONE', 'Finished'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
    
class Habit(models.Model):
    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)  # Par exemple : "quotidien", "hebdomadaire"
    daily_tracking = models.JSONField(default=dict)  # Utilisez un dictionnaire pour le suivi
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')

    def __str__(self):
        return self.name
