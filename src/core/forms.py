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
        fields = ['name', 'photo','goals', 'motivation', 'interests']
        widgets = {
            'interests': forms.TextInput(attrs={'placeholder': 'E.g., Productivity, Stress Management'}),
        }
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
    
    name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)
        

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 6, 'cols': 50, 'placeholder': 'Écris tes notes ici...'})
        }