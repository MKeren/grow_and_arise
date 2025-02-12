from django.contrib import admin
from .models import Note, UserProfile

admin.site.register(UserProfile)
admin.site.register(Note)
