from django.contrib.auth.models import AbstractUser,User
from django.db import models


class UserProfile(models.Model):
    INTEREST_CHOICES = [
        ('personal_development', 'Personal Development'),
        ('productivity', 'Productivity'),
        ('stress_management', 'Stress Management'),
        ('family', 'Family'),
        ('faith', 'Christian Faith'),
        ('health', 'Health'),
        ('studies', 'Studies'),
        ('self_care', 'Self Care'),
        ('mindfulness', 'Mindfulness'),
        ('career_growth', 'Career Growth'),
        ('others', 'Others'),

    ]

    interests = models.CharField(max_length=100,choices=INTEREST_CHOICES, default="self_care" ,unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, null=True) 
    photo = models.ImageField(upload_to='', blank=True, null=True)
    #photo = models.ImageField(upload_to='profiles', blank=True, null=True)

    goals = models.TextField(blank=True, null=True)
    motivation = models.IntegerField(blank=True, null=True)
    #interests = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        #return self.name
        return self.name or f"UserProfile for {self.user.username}"

    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associe la note à un utilisateur
    text = models.TextField()  # Le texte de la note
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création automatique

    def __str__(self):
        return f"Note de {self.user.username} - {self.created_at}"