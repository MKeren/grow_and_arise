from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, Habit
from .forms import TaskForm, HabitForm
from django.views.generic.edit import CreateView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required


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

def self_evaluation(request):
    return render(request, 'tracker/self_evaluation.html', {'title': _('Auto-évaluation')})

def smart_method(request):
    return render(request, 'tracker/smart_method.html', {'title': _('La Méthode SMART')})

def no_procrastination(request):
    return render(request, 'tracker/no_procrastination.html', {'title': _('Conseils pour ne plus procrastiner')})
