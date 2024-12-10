from django.urls import include, path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),


    path('prayer-room/', views.prayer_room, name='prayer_room'),
    path('meditation-lecture/', views.meditation_lecture, name='meditation_lecture'),
    path('meditation-notes/', views.meditation_notes, name='meditation_notes'),


    #path('home/', views.home, name='home'),
    path('register/', views.signup_view, name='register'),
    path('change-language/', views.change_language, name='change_language'),
    path('debug/', views.debug_language, name='debug'),
    

    path('accounts/', include('allauth.urls')),  # URLs pour l'authentification sociale
    path('login/', views.login_register_view, name='login'),
    path('register/', views.login_register_view, name='register'),

]


