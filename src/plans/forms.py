from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description']  # Champs à remplir dans le formulaire
