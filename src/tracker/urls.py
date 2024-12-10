from django.urls import path
from . import views  # Nous importons les vues pour chaque route

app_name = 'tracker'

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('create_task/', views.create_task, name='create_task'),
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/create/', views.create_habit, name='create_habit'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('smart-method/', views.smart_method, name='smart_method'),
    path('no-procrastination/', views.no_procrastination, name='no_procrastination'),
    path('self-evaluation/', views.self_evaluation, name='self_evaluation'),
]

