from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, Habit
from .forms import HabitTrackingForm, TaskForm, HabitForm
from django.views.generic.edit import CreateView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from .models import Habit,HabitCategory
from datetime import timedelta
from django.utils.timezone import now

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status']  # Les champs à inclure dans le formulaire
    template_name = 'tracker/task_form.html'
    success_url = '/tracker/tasks/'

# Liste des tâches
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tracker/task_list.html', {'tasks': tasks})

# Créer une tâche
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tracker/create_task.html', {'form': form})

def self_evaluation(request):
    return render(request, 'tracker/self_evaluation.html', {'title': _('Auto-évaluation')})

def smart_method(request):
    return render(request, 'tracker/smart_method.html', {'title': _('La Méthode SMART')})

def no_procrastination(request):
    return render(request, 'tracker/no_procrastination.html', {'title': _('Conseils pour ne plus procrastiner')})

# Liste des habitudes
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'tracker/habit_list.html', {'habits': habits})

# Créer une habitude
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'tracker/create_habit.html', {'form': form})

# Mettre à jour le suivi d'une habitude
@login_required
def update_tracking_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        tracking_form = HabitTrackingForm(request.POST)
        if tracking_form.is_valid():
            tracking = tracking_form.save(commit=False)
            tracking.habit = habit
            tracking.save()
            return redirect("habit_list")
    else:
        tracking_form = HabitTrackingForm()

    context = {
        "habit": habit,
        "tracking_form": tracking_form,
    }
    return render(request, "tracker/update_tracking.html", context)

@login_required
def habit_report_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    tracking_data = habit.tracking.all()

    if habit.frequency == "daily":
        report_range = [habit.created_at.date() + timedelta(days=i) for i in range((now().date() - habit.created_at.date()).days + 1)]
    elif habit.frequency == "weekly":
        report_range = [habit.created_at.date() + timedelta(weeks=i) for i in range(((now().date() - habit.created_at.date()).days // 7) + 1)]
    elif habit.frequency == "monthly":
        report_range = [habit.created_at.date().replace(day=1) + timedelta(days=30 * i) for i in range(((now().date().year - habit.created_at.date().year) * 12 + now().date().month - habit.created_at.date().month) + 1)]
    else:
        report_range = [habit.created_at.date().replace(day=1, month=1) + timedelta(days=365 * i) for i in range(now().date().year - habit.created_at.date().year + 1)]

    progress = {date: tracking_data.filter(date=date).exists() for date in report_range}

    # Calculate completed and missed days for the chart
    completed_count = sum(progress.values())
    missed_count = len(progress) - completed_count

    context = {
        "habit": habit,
        "report_range": report_range,
        "progress": progress,
        "completed_count": completed_count,
        "missed_count": missed_count,
    }
    return render(request, "tracker/habit_report.html", context)

def load_categories():
    categories = ["Food", "Self-care", "Perfect Morning", "Self-development", "Family"]
    for category in categories:
        HabitCategory.objects.get_or_create(name=category)
