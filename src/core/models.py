from django.contrib.auth.models import AbstractUser,User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, null=True) 
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    goals = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associe la note à un utilisateur
    text = models.TextField()  # Le texte de la note
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création automatique

    def __str__(self):
        return f"Note de {self.user.username} - {self.created_at}"