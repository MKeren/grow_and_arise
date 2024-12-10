from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')

    def __str__(self):
        return self.title

class Step(models.Model):
    plan = models.ForeignKey(Plan, related_name='steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Étape {self.order} : {self.title} ({self.plan.title})"
