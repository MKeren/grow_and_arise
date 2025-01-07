from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime, timedelta


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
    CATEGORY_CHOICES = [
        ('sport', 'Sport'),
        ('family', 'Family'),
        ('self_development', 'Self-development'),
        ('perfect_morning', 'Perfect Morning'),
        ('self_care', 'Self-care'),
        ('food', 'Food'),
    ]

    name = models.CharField(max_length=100,choices=CATEGORY_CHOICES, default="self_care" ,unique=True)

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
    category = models.ForeignKey(HabitCategory, on_delete=models.CASCADE,default=1)
    #category = models.ForeignKey(HabitCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="habits")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_frequency = models.PositiveIntegerField(help_text="Target times for the chosen frequency",null=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default="daily")
    motivation = models.TextField(help_text="What will motivate me?")
    created_at = models.DateTimeField(auto_now_add=True)
    occurrences = models.IntegerField(default="2")

    def __str__(self):
        return self.name
    
    def get_tracking_data(self):
        # Génère un dictionnaire contenant les dates et les états des occurrences
        tracking_data = {}
        today = datetime.today().date()

        for i in range(self.occurrences):
            date = today - timedelta(days=i)
            # Simulez le statut d'achèvement (True/False) pour cet exemple
            tracking_data[date] = [False] * self.occurrences

        return tracking_data

    def calculate_progress(self):
        # Calcule le pourcentage de complétions
        tracking_data = self.get_tracking_data()
        total = self.occurrences * len(tracking_data)
        completed = sum([sum(statuses) for statuses in tracking_data.values()])
        return (completed / total) * 100 if total > 0 else 0

class HabitTracking(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="tracking")
    date = models.DateField(default=now)
    completed = models.BooleanField(default=False)
    occurrence_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.habit.name} on {self.date}"
    
    class Meta:
        unique_together = ['habit', 'date', 'occurrence_count']
    
class AutoEvaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur qui a rempli l'évaluation
    date = models.DateField(auto_now_add=True)  # Date de l'évaluation
    mots = models.CharField(max_length=200)  # Les 3 mots
    sentiment = models.TextField()  # Comment tu te sens
    amelioration = models.TextField()  # Comment améliorer ce sentiment
    fiers = models.TextField()  # Les 5 choses dont tu es fière
    difficultes = models.TextField()  # Difficultés rencontrées
    message = models.TextField()  # Message à Dieu

    def __str__(self):
        return f"Évaluation du {self.date} par {self.user.username}"
