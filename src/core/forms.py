from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, User
from .models import UserProfile

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'photo', 'goals']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 6, 'cols': 50, 'placeholder': 'Écris tes notes ici...'})
        }
