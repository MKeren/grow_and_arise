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
        interests = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(),
        empty_label="--- Choisissez ---",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
        fields = ['name', 'photo','goals', 'motivation', 'interests']
        widgets = {
            #'interests': forms.TextInput(attrs={'placeholder': 'E.g., Productivity, Stress Management'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your goals...'}),
            'motivation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Motivation Level'}),
            #'interests': forms.CheckboxSelectMultiple(attrs={'class': 'form-check', 'placeholder': 'E.g., Productivity, Stress Management'}),
        }
    
    
    name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)
        

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 6, 'cols': 50, 'placeholder': 'Écris tes notes ici...'})
        }