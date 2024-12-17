from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import Plan
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


def daily_planning(request):
    return render(request, 'plans/daily_planning.html', {'title': _('Planning de la Journée')})

def daily_routines(request):
    return render(request, 'plans/daily_routines.html', {'title': _('Mes Routines Journalières')})

def finance_review(request):
    return render(request, 'plans/finance_review.html', {'title': _('Bilan de Mes Finances')})

def daily_planning(request):
    days = ["MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE"]
    return render(request, 'plans/daily_planning.html', {'days': days})