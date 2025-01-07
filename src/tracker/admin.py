from django.contrib import admin
from .models import AutoEvaluation, HabitCategory, HabitTracking, Task, Habit

admin.site.register(Task)
admin.site.register(Habit)
admin.site.register(HabitCategory)
admin.site.register(HabitTracking)


@admin.register(AutoEvaluation)
class AutoEvaluationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mots')  # Colonnes affichées dans l'admin
    search_fields = ('user__username', 'mots')  # Recherche par utilisateur et mots
    list_filter = ('date',)  # Filtrage par date