from django.urls import path
from . import views  # Nous importons les vues pour chaque route

app_name = 'tracker'

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('create_task/', views.create_task, name='create_task'),

    path('habits/', views.habit_list, name='habits'),
    #path('habit_tracker/', views.habit_tracker, name='habit_tracker'),
    path('create/', views.create_habit, name='create_habit'),
    path('update-tracking/<int:habit_id>/', views.update_tracking_view, name='update_tracking'),
    path('<int:habit_id>/report/', views.habit_report_view, name='habit_report'),
    path('load_categories/', views.load_categories, name='load_categories'),

    path('tasks/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('smart-method/', views.smart_method, name='smart_method'),
    path('no-procrastination/', views.no_procrastination, name='no_procrastination'),
    path('pomodoro/', views.pomodoro_view, name='pomodoro'),
    
    path('self-evaluation/', views.self_evaluation, name='self_evaluation'),
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
    path('evaluations/<int:evaluation_id>/', views.evaluation_detail, name='evaluation_detail'),
]

