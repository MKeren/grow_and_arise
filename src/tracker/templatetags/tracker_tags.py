# tracker_tags.py
from django import template
from ..models import Habit

register = template.Library()

@register.filter
def get_day_status(habit_id, day):
    # Récupérer le suivi de l'habitude pour l'utilisateur connecté et le jour
    tracking = Habit.objects.filter(habit_id=habit_id, date=day).first()
    return tracking.completed if tracking else False
