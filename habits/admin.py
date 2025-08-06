from django.contrib import admin
from .models import Habit, HabitEntry

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'created_at', 'is_active']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['name', 'user__username']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)
    
@admin.register(HabitEntry)
class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'completed', 'created_at']
    list_filter = ['completed', 'date', 'habit__frequency']
    search_fields = ['habit__name', 'notes']

