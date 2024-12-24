from django import forms
from .models import AutoEvaluation, HabitTracking, Task, Habit

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description", "category", "target_frequency", "frequency", "motivation"]
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 3, "placeholder": "What will motivate me?"}),
            "frequency": forms.Select(),
            "category": forms.Select(),
            "target_frequency": forms.NumberInput(attrs={"placeholder": "Enter a numeric target"}),
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