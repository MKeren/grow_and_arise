from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import AutoEvaluation, HabitTracking, Task, Habit
from .forms import EvaluationForm, HabitTrackingForm, TaskForm, HabitForm
from django.views.generic.edit import CreateView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from .models import Habit,HabitCategory
from datetime import timedelta, timezone
from django.utils.timezone import now
from django.contrib import messages

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status']  # Les champs à inclure dans le formulaire
    template_name = 'tracker/task_form.html'
    success_url = '/tracker/tasks/'

#///////TASKS///////////////////////////////
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

#///////SELF EVALUATION///////////////////////////////

@login_required
def self_evaluation(request):
    if request.method == 'POST':
        print(request.POST)  # Affiche les données reçues
        
        mots_1 = request.POST.get('mots_1', '').strip()
        mots_2 = request.POST.get('mots_2', '').strip()
        mots_3 = request.POST.get('mots_3', '').strip()
        sentiment = request.POST.get('sentiment', '').strip()
        amelioration = request.POST.get('amelioration', '').strip()
        fiers = request.POST.get('fiers', '').strip()
        difficultes = request.POST.get('difficultes', '').strip()
        message = request.POST.get('message', '').strip()

        # Combine les 3 mots en une seule chaîne pour correspondre au champ `mots`
        mots = ', '.join(filter(None, [mots_1, mots_2, mots_3]))

        # Crée une nouvelle instance AutoEvaluation et enregistre-la
        evaluation = AutoEvaluation.objects.create(
            user=request.user,
            mots=mots,
            sentiment=sentiment,
            amelioration=amelioration,
            fiers=fiers,
            difficultes=difficultes,
            message=message
        )
        evaluation.save()

        return redirect('tracker:evaluation_list')  # Redirige vers la liste des évaluations

    return render(request, 'tracker/self_evaluation.html')

@login_required
def evaluation_list(request):
    # Récupérer toutes les évaluations de l'utilisateur connecté, triées par date
    evaluations = AutoEvaluation.objects.filter(user=request.user).order_by('-date')
    
    # Passer les évaluations au template
    return render(request, 'tracker/evaluation_list.html', {'evaluations': evaluations})

@login_required
def evaluation_detail(request, evaluation_id):
    # Récupérer l'évaluation par son ID et s'assurer qu'elle appartient à l'utilisateur connecté
    evaluation = get_object_or_404(AutoEvaluation, id=evaluation_id, user=request.user)
    
    return render(request, 'tracker/evaluation_detail.html', {'evaluation': evaluation})

#///////TIPS///////////////////////////////

def smart_method(request):
    return render(request, 'tracker/smart_method.html', {'title': _('La Méthode SMART')})

def no_procrastination(request):
    return render(request, 'tracker/no_procrastination.html', {'title': _('Conseils pour ne plus procrastiner')})

def pomodoro_view(request):
    return render(request, 'tracker/pomodoro.html')
#///////HABITS///////////////////////////////

def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'tracker/habit_list.html', {'habits': habits})

def reate_habit(request):
    # Crée les catégories si elles n'existent pas
    category_names = ["Food", "Self-care", "Perfect Morning", "Self-development", "Family"]
    for name in category_names:
        HabitCategory.objects.get_or_create(name=name)

    # Récupère toutes les catégories existantes
    categories = HabitCategory.objects.all()

    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('tracker:habits')
    else:
        form = HabitForm()

    # Passe les catégories au template
    return render(request, 'tracker/create_habit.html', {'categories': categories})

def create_habit(request):
    # Crée les catégories par défaut si elles n'existent pas
    default_categories = ["Food", "Self-care", "Perfect Morning", "Self-development", "Family"]
    for name in default_categories:
        HabitCategory.objects.get_or_create(name=name)

    # Récupère toutes les catégories existantes
    categories = HabitCategory.objects.all()

    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user  # Associe l'utilisateur actuel à l'habitude
            habit.save()
            return redirect("tracker:habits")
    else:
        form = HabitForm()

    return render(request, "tracker/create_habit.html", {"form": form, "categories": categories})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect("tracker:habits")

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
    #progress = habit.get_progress()

    # Préparer les données pour le tableau
    #progress_data = []
    #for date, completed_list in progress.items():
        #progress_data.append({
            #'date': date,
            #'completed': completed_list,
            #'progress_percent': (sum(completed_list) / len(completed_list)) * 100 if completed_list else 0,
        #})
    

    # Déterminer la plage de dates selon la fréquence
    if habit.frequency == "daily":
        report_range = [habit.created_at.date() + timedelta(days=i) 
                       for i in range((now().date() - habit.created_at.date()).days + 1)]
    elif habit.frequency == "weekly":
        report_range = [habit.created_at.date() + timedelta(weeks=i) 
                       for i in range(((now().date() - habit.created_at.date()).days // 7) + 1)]
    elif habit.frequency == "monthly":
        report_range = [habit.created_at.date().replace(day=1) + timedelta(days=30 * i) 
                       for i in range(((now().date().year - habit.created_at.date().year) * 12 
                                     + now().date().month - habit.created_at.date().month) + 1)]
    else:  # yearly
        report_range = [habit.created_at.date().replace(day=1, month=1) + timedelta(days=365 * i) 
                       for i in range(now().date().year - habit.created_at.date().year + 1)]

    # Initialiser le dictionnaire de progression
    progress = {}
    total_completed = 0
    total_possible = 0

    # Pour chaque date dans la plage
    for date in report_range:
        # Récupérer tous les suivis pour cette date
        day_tracking = tracking_data.filter(date=date).order_by('occurrence_count')
        
        # Créer la liste des checkboxes pour cette date
        checkboxes = []
        completed_today = 0
        
        # Pour chaque occurrence possible
        for i in range(1, habit.occurrences + 1):
            # Vérifier si cette occurrence existe dans le tracking
            is_completed = day_tracking.filter(occurrence_count=i).exists()
            checkboxes.append({'completed': is_completed})
            if is_completed:
                completed_today += 1
        
        # Calculer le pourcentage de progression pour ce jour
        day_progress = (completed_today / habit.occurrences * 100) if habit.occurrences > 0 else 0
        
        # Mettre à jour les totaux
        total_completed += completed_today
        total_possible += habit.occurrences
        
        # Stocker les informations pour cette date
        progress[date] = {
            'checkboxes': checkboxes,
            'progress': round(day_progress, 2)
        }

    # Calculer les statistiques globales pour le graphique
    total_days = len(report_range)
    completed_count = total_completed
    missed_count = total_possible - total_completed

     # Ajouter une plage basée sur le nombre d'occurrences
    occurrences_range = range(habit.occurrences)

    context = {
        "habit": habit,
        "progress": progress,
        "completed_count": completed_count,
        "missed_count": missed_count,
        'occurrences_range': occurrences_range,  # Ajout de la plage au contexte
        #"progress_data": progress_data,  # Liste des données préparées
        #"occurrences_range": range(habit.occurrences),
        #"completed_count": sum(len(c['completed']) for c in progress_data),
        #"missed_count": habit.occurrences * len(progress_data) - sum(len(c['completed']) for c in progress_data),
   
    }

    return render(request, "tracker/habit_report.html", context)

def load_categories():
    categories = ["Food", "Self-care", "Perfect Morning", "Self-development", "Family"]
    for category in categories:
        HabitCategory.objects.get_or_create(name=category)

def udate_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            #return redirect('tracker:habits')
            return redirect('tracker:habit_report', habit_id=habit.id)
    else:
        form = HabitForm(instance=habit)
        
    # Transmettre toutes les catégories au contexte
    categories = HabitCategory.objects.all()
    
    return render(request, 'tracker/habit_report.html', {
        'form': form,
        'habit': habit,  # L'habitude actuelle, si elle existe
        'categories': categories,  # Les catégories globales
    })

def update_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            #return JsonResponse({'success': True})
            return redirect('tracker:habit_report', habit_id=habit.id)
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = HabitForm(instance=habit)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'tracker/update_habit_form.html', {'form': form})
           

        return render(request, 'tracker/update_tracking.html', {'form': form, 'habit': habit})
#////////////////////////////////////////////
