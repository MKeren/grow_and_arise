from django.urls import include, path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_update/', views.update_profile, name='profile_update'),


    path('prayer-room/', views.prayer_room, name='prayer_room'),
    path('meditation-lecture/', views.meditation_lecture, name='meditation_lecture'),
    path('meditation-notes/', views.meditation_notes, name='meditation_notes'),


    path('change-language/', views.change_language, name='change_language'),
    path('debug/', views.debug_language, name='debug'),
    

    #path('accounts/', include('allauth.urls')),  # URLs pour l'authentification sociale
    path('logout/', views.logout_view, name="logout"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



