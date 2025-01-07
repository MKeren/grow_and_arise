from django import forms
from .models import AutoEvaluation, HabitCategory, HabitTracking, Task, Habit

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class HabitForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=HabitCategory.objects.all(),
        empty_label="--- Choisissez une catégorie ---",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Habit
        fields = ['name', 'motivation', 'category', 'frequency', 'occurrences', "description",
            "target_frequency",]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de l'habitude"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description facultative"}),
            "target_frequency": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre cible pour la fréquence choisie"}),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "motivation": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Quelle est votre motivation ?"}),
            "occurrences": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre d'occurrences"}),
        }


class abitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "category",
            "name",
            "description",
            "target_frequency",
            "frequency",
            "motivation",
            "occurrences",
        ]
    
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de l'habitude"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description facultative"}),
            "target_frequency": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre cible pour la fréquence choisie"}),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "motivation": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Quelle est votre motivation ?"}),
            "occurrences": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre d'occurrences"}),
        }

class HabitTrackingForm(forms.ModelForm):
    class Meta:
        model = HabitTracking
        fields = ["date", "completed"]

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = AutoEvaluation
        fields = ['mots', 'sentiment', 'amelioration', 'fiers', 'difficultes', 'message']
        widgets = {
            'mots': forms.Textarea(attrs={'class': 'form-control'}),
            'sentiment': forms.Textarea(attrs={'class': 'form-control'}),
            'amelioration': forms.Textarea(attrs={'class': 'form-control'}),
            'fiers': forms.Textarea(attrs={'class': 'form-control'}),
            'difficultes': forms.Textarea(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }