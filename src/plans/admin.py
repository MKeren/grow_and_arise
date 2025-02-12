from django.contrib import admin

from .models import Plan, Step, ThingsToAchieve

admin.site.register(ThingsToAchieve)
admin.site.register(Step)

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    inlines = [StepInline]


