from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import json

# store habits
class Habit(models.Model):

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('weekends', 'Weekends Only'),
        ('3x_week', '3x per Week'),
        ('custom', 'Custom Plan'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    target_days = models.IntegerField(default=21)  # For custom plans
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    from datetime import date, timedelta

    def get_current_streak(self):
        today = date.today()
        current_day = today
        streak = 0

        if self.created_at.date() > today:
            return 0

        while current_day >= self.created_at.date():
            if not self.should_be_done_on_date(current_day):
                current_day -= timedelta(days=1)
                continue

            entry = HabitEntry.objects.filter(habit=self, date=current_day).first()

            if entry and entry.completed:
                streak += 1
            else:
                if current_day == today:
                    current_day -= timedelta(days=1)
                    continue
                break

            current_day -= timedelta(days=1)

        return streak
# check that habit is done on specific day or not
    def should_be_done_on_date(self, check_date):
        if self.frequency == 'daily':
            return True
        elif self.frequency == 'weekly':
            return check_date.weekday() == 0  # Monday
        elif self.frequency == 'weekends':
            return check_date.weekday() in [5, 6]  # Saturday, Sunday
        elif self.frequency == '3x_week':
            return check_date.weekday() in [0, 2, 4]  # Mon, Wed, Fri
        elif self.frequency == 'custom':
            days_since_created = (check_date - self.created_at.date()).days
            return days_since_created < self.target_days
        return False
 # percentage for completed habit   
    def get_progress_percentage(self):
        if self.frequency == 'custom':
            days_since_created = (date.today() - self.created_at.date()).days
            completed_days = HabitEntry.objects.filter(
                habit=self, 
                completed=True,
                date__gte=self.created_at.date(),
                date__lte=date.today()
            ).count()
            
            if self.target_days > 0:
                return min((completed_days / self.target_days) * 100, 100)
        else:
            week_start = date.today() - timedelta(days=date.today().weekday())
            week_end = week_start + timedelta(days=6)
            
            expected_days = sum(1 for i in range(7) 
                              if self.should_be_done_on_date(week_start + timedelta(days=i)))
            
            completed_days = HabitEntry.objects.filter(
                habit=self,
                completed=True,
                date__gte=week_start,
                date__lte=week_end
            ).count()
            
            if expected_days > 0:
                return (completed_days / expected_days) * 100
        
        return 0
# if streak was broken yesterday
    def broke_streak_yesterday(self):
        yesterday = timezone.localdate() - timedelta(days=1)

        if self.created_at.date() >= timezone.localdate():
            return False

        if not self.should_be_done_on_date(yesterday):
            return False

        y_entry = HabitEntry.objects.filter(habit=self, date=yesterday).first()
        if not y_entry:
            return True  
    
        return not y_entry.completed
# habit entry model
class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.habit.name} - {self.date} ({'✓' if self.completed else '✗'})"
    
    