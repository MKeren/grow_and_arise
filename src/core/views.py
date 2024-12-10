from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from plans.models import Plan
from tracker.models import Task
from core.forms import NoteForm, UserCreationForm, UserProfileForm
from core.models import Note, UserProfile
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import get_language

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def Login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Vérifier les identifiants
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Vous êtes connecté avec succès!")
            return redirect("home")  # Redirige vers la page d'accueil
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")

    return render(request, "core/login.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Django User Model requires username or custom user with email
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Connexion réussie!")
            return redirect("home")  # Remplacez par l'URL de votre page d'accueil
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")
    
    return render(request, "core/login.html")

@login_required
def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérification des champs
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
        else:
            # Création du nouvel utilisateur
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            user.save()
            messages.success(request, "Compte créé avec succès! Connectez-vous maintenant.")
            return redirect("login")

    return render(request, "core/register.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect("login")


def change_language(request):
    lang_code = request.GET.get('lang', settings.LANGUAGE_CODE)
    if lang_code in dict(settings.LANGUAGES):
        activate(lang_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))

def debug_language(request):
    current_language = get_language()
    return HttpResponse(f"Current language: {current_language}")

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def Home(request):
    plans = Plan.objects.filter(creator=request.user)
    tasks = Task.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'core/home.html', {'plans': plans, 'tasks': tasks})

#@login_required
def home(request):
    return render(request, "core/home.html", {"user": request.user})


def index(request):
    return render(request, "core/index.html", {"user": request.user})

def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'form': form})

def prayer_room(request):
    return render(request, 'core/prayer_room.html', {'title': _('My Prayer Room')})

def meditation_lecture(request):
    return render(request, 'core/meditation_lecture.html')

@login_required
def meditation_notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            # Sauvegarde de la note avec l'utilisateur connecté
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('meditation_notes')  # Redirige vers la même page après la soumission
    else:
        form = NoteForm()

    # Récupère toutes les notes de l'utilisateur connecté
    notes = Note.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/meditation_notes.html', {'form': form, 'notes': notes})
