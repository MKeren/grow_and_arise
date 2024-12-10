from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet
from plans import views

#router = DefaultRouter()
#router.register(r'plans', PlanViewSet)

app_name = 'plans'

urlpatterns = [
    #path('', include(router.urls)),

    path('create/', views.create_plan, name='create_plan'),
    path('<int:pk>/', views.plan_detail, name='plan_detail'), 
    path('daily-planning/', views.daily_planning, name='daily_planning'),
    path('daily-routines/', views.daily_routines, name='daily_routines'),
    path('finance-review/', views.finance_review, name='finance_review'),
    path('plan_list/', views.plan_list, name='plan_list'),
    
]