from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import Plan, ThingsToAchieve
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import PlanForm
from django.utils.translation import gettext as _

class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class PlanListAPIView(APIView):
    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
# Vue pour afficher la liste des plans
def plan_list(request):
    plans = Plan.objects.all()  # Récupérer tous les plans de la base de données
    return render(request, 'plans/plan_list.html', {'plans': plans})

# Vue pour créer un nouveau plan
def create_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_list')  # Rediriger vers la liste des plans après création
    else:
        form = PlanForm()  # Afficher le formulaire vide pour créer un plan
    return render(request, 'plans/create_plan.html', {'form': form})

# Vue pour afficher les détails d'un plan (facultatif, si tu veux une page de détails)
def plan_detail(request, pk):
    plan = Plan.objects.get(pk=pk)  # Récupérer un plan spécifique
    return render(request, 'plans/plan_detail.html', {'plan': plan})


#def daily_planning(request):
    return render(request, 'plans/daily_planning.html', {'title': _('Planning de la Journée')})

def daily_routines(request):
    return render(request, 'plans/daily_routines.html', {'title': _('Mes Routines Journalières')})

def finance_review(request):
    return render(request, 'plans/finance_review.html', {'title': _('Bilan de Mes Finances')})

def daily_planning(request):
    days = ["TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    return render(request, 'plans/daily_planning.html', {'days': days})

def my_view(request):
    my_string = "lundi,mardi,mercredi"  # Exemple
    split_days = my_string.split(",")
    return render(request, "plans/template.html", {"split_days": split_days})

def current_month(request):
    return render(request, 'plans/current_month.html')

def previous_month(request):
    return render(request, 'plans/previous_month.html')

def things_to_achieve(request):
    if request.method == 'POST':
        main_goal = request.POST.get('main_goal', '').strip()
        steps = request.POST.get('steps', '').strip()
        motivation = request.POST.get('motivation', '').strip()
        deadline = request.POST.get('deadline', '').strip()

        # Sauvegarde dans la base de données
        ThingsToAchieve.objects.create(
            user=request.user,
            main_goal=main_goal,
            steps=steps,
            motivation=motivation,
            deadline=deadline
        )
        return HttpResponseRedirect('/success-page/')  # Redirige après soumission

    return render(request, 'plans/things_to_achieve.html')