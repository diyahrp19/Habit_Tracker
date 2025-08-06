#!/usr/bin/env python
"""
Script to populate the database with sample motivational tips
Run this after running migrations: python setup_data.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
django.setup()

from habits.models import MotivationalTip

def create_motivational_tips():
    tips = [
        {
            'text': 'The secret of getting ahead is getting started.',
            'author': 'Mark Twain'
        },
        {
            'text': 'Success is the sum of small efforts repeated day in and day out.',
            'author': 'Robert Collier'
        },
        {
            'text': 'We are what we repeatedly do. Excellence, then, is not an act, but a habit.',
            'author': 'Aristotle'
        },
        {
            'text': 'The groundwork for all happiness is good health.',
            'author': 'Leigh Hunt'
        },
        {
            'text': 'Take care of your body. It\'s the only place you have to live.',
            'author': 'Jim Rohn'
        },
        {
            'text': 'A journey of a thousand miles begins with a single step.',
            'author': 'Lao Tzu'
        },
        {
            'text': 'The best time to plant a tree was 20 years ago. The second best time is now.',
            'author': 'Chinese Proverb'
        },
        {
            'text': 'Don\'t watch the clock; do what it does. Keep going.',
            'author': 'Sam Levenson'
        },
        {
            'text': 'The only impossible journey is the one you never begin.',
            'author': 'Tony Robbins'
        },
        {
            'text': 'Your future is created by what you do today, not tomorrow.',
            'author': 'Robert Kiyosaki'
        }
    ]
    
    created_count = 0
    for tip_data in tips:
        tip, created = MotivationalTip.objects.get_or_create(
            text=tip_data['text'],
            defaults={'author': tip_data['author']}
        )
        if created:
            created_count += 1
    
    print(f'Created {created_count} motivational tips')

if __name__ == '__main__':
    create_motivational_tips()
