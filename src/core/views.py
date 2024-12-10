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


def login_register_view(request):
    """
    Handles login and register functionality.
    """
    if request.method == "POST":
        # Login form submission
        if "login" in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('home')
        # Register form submission
        elif "register" in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
        register_form = UserCreationForm()

    return render(request, "auth_page.html", {
        "login_form": form,
        "register_form": register_form,
    })

def change_language(request):
    lang_code = request.GET.get('lang', settings.LANGUAGE_CODE)
    if lang_code in dict(settings.LANGUAGES):
        activate(lang_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.utils.translation import get_language

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

def home(request):
    plans = Plan.objects.filter(creator=request.user)
    tasks = Task.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'core/index.html', {'plans': plans, 'tasks': tasks})

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
