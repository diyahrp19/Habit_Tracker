from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
# from django.utils import timezone
# from django.db.models import Count, Q
from datetime import date, timedelta
import csv
import json
from .models import Habit, HabitEntry
from .forms import CustomUserCreationForm, HabitForm, HabitEntryForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    today = date.today()
    habit_data = []
    for habit in habits:
        entry, created = HabitEntry.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'completed': False}
    )

        scheduled_today = habit.should_be_done_on_date(today)  # ✅ Define it here

        yesterday = date.today() - timedelta(days=1)
        scheduled_yesterday = habit.should_be_done_on_date(yesterday)
        today_entry = HabitEntry.objects.get(habit=habit, date=today)

        if habit.created_at.date() >= yesterday:
            broke_streak_yesterday = False
        elif not scheduled_yesterday:
            broke_streak_yesterday = False
        else:
            try:
                yesterday_entry = HabitEntry.objects.get(habit=habit, date=yesterday)
                broke_streak_yesterday = not yesterday_entry.completed and not today_entry.completed
            except HabitEntry.DoesNotExist:
                broke_streak_yesterday = not today_entry.completed

        habit_data.append({
            'habit': habit,
            'entry': entry,
            'streak': habit.get_current_streak(),
            'progress': habit.get_progress_percentage(),
            'scheduled_today': scheduled_today,  # ✅ Now it's safe to use
            'streak_broken': broke_streak_yesterday,
     })
    
    context = {
        'habit_data': habit_data,
        'today': today,
    }
    
    return render(request, 'habits/dashboard.html', context)

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f'Habit "{habit.name}" created successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm()
    
    return render(request, 'habits/create_habit.html', {'form': form})

@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Habit "{habit.name}" updated successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    
    return render(request, 'habits/edit_habit.html', {'form': form, 'habit': habit})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == 'POST':
        habit_name = habit.name

        soft_delete = True  # Change to False if you want hard delete

        if soft_delete:
            # Hide the habit but keep its data
            habit.is_active = False
            habit.save()
            messages.success(request, f'Habit "{habit_name}" was deactivated (soft deleted).')
        else:
            # Remove habit + all related HabitEntry records
            habit.delete()
            messages.success(request, f'Habit "{habit_name}" was permanently deleted with all entries.')

        return redirect('dashboard')

    return render(request, 'habits/delete_habit.html', {'habit': habit})

@login_required
def toggle_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        today = date.today()
        
        entry, created = HabitEntry.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'completed': False}
        )
        
        entry.completed = not entry.completed
        entry.save()
        
        return JsonResponse({
            'success': True,
            'completed': entry.completed,
            'streak': habit.get_current_streak(),
            'progress': habit.get_progress_percentage(),
        })
    
    return JsonResponse({'success': False})

@login_required
def update_notes(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        today = date.today()
        notes = request.POST.get('notes', '')
        
        entry, created = HabitEntry.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'completed': False}
        )
        
        entry.notes = notes
        entry.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def analytics(request):
    habits = Habit.objects.filter(user=request.user)
    habit_performance = []
    today = date.today()
    start_date = today - timedelta(days=30)

    for habit in habits:
        completed_days = 0
        scheduled_days = 0

        for i in range(31):  # Loop through the last 31 days
            current_date = start_date + timedelta(days=i)

            # Only count if habit should be done that day
            if habit.should_be_done_on_date(current_date):
                scheduled_days += 1

                # Check if that scheduled entry was completed
                if HabitEntry.objects.filter(habit=habit, date=current_date, completed=True).exists():
                    completed_days += 1

        # Avoid divide-by-zero and retain float
        percentage = (completed_days / scheduled_days) * 100 if scheduled_days > 0 else 0.0

        habit_performance.append({
            'name': habit.name,
            'percentage': habit.get_progress_percentage()  # Rounded to 2 decimals
        })

    return render(request, 'habits/analytics.html', {
        'habits': habits,
        'habit_performance': json.dumps(habit_performance)
    })

@login_required
def export_csv(request):
    filename = f"{request.user.username}_habits_{date.today().strftime('%Y-%m-%d')}.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    
    # Write header with updated columns
    writer.writerow([
        'Habit Name', 
        'Frequency', 
        'Status',
        'Created Date',
        'Current Streak',
        'Progress (%)',
        'Last Completed Date',
        'Notes'
    ])

    habits = Habit.objects.filter(
        user=request.user,
        is_active=True
    ).prefetch_related('habitentry_set')

    for habit in habits:
        # Get the last completed entry
        last_completed = habit.habitentry_set.filter(completed=True).order_by('-date').first()
        last_completed_date = last_completed.date if last_completed else "Never"

        writer.writerow([
            f"{habit.name}",
            habit.get_frequency_display(),
            "Active" if habit.is_active else "Inactive",
            habit.created_at.date().strftime('%Y-%m-%d'),
            habit.get_current_streak(),
            f"{habit.get_progress_percentage():.0f}",  # Using the model's progress method
            last_completed_date.strftime('%Y-%m-%d') if last_completed_date != "Never" else "Never",
            "; ".join([e.notes for e in habit.habitentry_set.all() if e.notes])
        ])

    return response
