from django.test import TestCase

from tracker.forms import HabitForm

# Create your tests here.
form = HabitForm(data={
    'name': 'Faire du sport',
    'motivation': 'Rester en bonne santé',
    'category': 1,  # Assurez-vous qu'une catégorie avec cet ID existe
    'frequency': 'daily',
    'occurrences': 5,
    'target_frequency': 10,
    'description': 'Une habitude pour améliorer ma condition physique',
})
assert form.is_valid(), form.errors
