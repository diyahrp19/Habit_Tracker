from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from habits.models import Habit, HabitEntry

class Command(BaseCommand):
    help = 'Reset daily habits at midnight'

    def handle(self, *args, **options):
        today = date.today()
        daily_habits = Habit.objects.filter(frequency='daily', is_active=True)
        
        created_count = 0
        for habit in daily_habits:
            entry, created = HabitEntry.objects.get_or_create(
                habit=habit,
                date=today,
                defaults={'completed': False}
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} daily habit entries for {today}'
            )
        )
