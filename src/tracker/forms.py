from django import forms
from .models import HabitTracking, Task, Habit

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