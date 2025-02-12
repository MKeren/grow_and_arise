from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet
from plans import views

#router = DefaultRouter()
#router.register(r'plans', PlanViewSet)

app_name = 'plans'

urlpatterns = [
    #path('', include(router.urls)),
    
    path('plan_list/', views.plan_list, name='plan_list'),
    path('create/', views.create_plan, name='create_plan'),
    path('<int:pk>/', views.plan_detail, name='plan_detail'), 

    path('daily-planning/', views.daily_planning, name='daily_planning'),
    path('daily-routines/', views.daily_routines, name='daily_routines'),
    path('things-to-achieve/', views.things_to_achieve, name='things_to_achieve'),
    path('success/', views.success_page, name='success_page'),

    path('finance-review/', views.finance_review, name='finance_review'),
    path('current_month/', views.current_month, name='current_month'),
    path('previous_month/', views.previous_month, name='previous_month'),

    
    

]