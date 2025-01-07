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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'core/login.html')

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

@login_required
def home(request):
    plans = Plan.objects.filter(creator=request.user)
    tasks = Task.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'core/home.html', {'plans': plans, 'tasks': tasks})

def index(request):
    return render(request, "core/index.html", {"user": request.user})

def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'form': form})

def update_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Logique pour mettre à jour l'utilisateur dans la base de données
            user = request.user
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.interests = form.cleaned_data['interests']
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Vos informations ont été mises à jour avec succès !")
            return redirect('profile')  # Redirection vers la page de profil
    else:
        form = UserProfileForm(initial={
            'name': request.user.name,
            'email': request.user.email,
            'interests': request.user.interests,  # Ajouter l'intérêt de l'utilisateur dans la base
        })

    return render(request, 'core/profile_update.html', {'form': form})

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
