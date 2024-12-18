from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


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
    

class HabitCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    category = models.ForeignKey(HabitCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="habits")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_frequency = models.PositiveIntegerField(help_text="Target times for the chosen frequency",null=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default="daily")
    motivation = models.TextField(help_text="What will motivate me?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HabitTracking(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="tracking")
    date = models.DateField(default=now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} on {self.date}"
