from rest_framework import serializers
from .models import Plan, Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'title', 'content', 'order']

class PlanSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'duration_days', 'steps']
