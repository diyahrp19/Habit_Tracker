from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Habits
    path('create/', views.create_habit, name='create_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('toggle/<int:habit_id>/', views.toggle_habit, name='toggle_habit'),
    path('notes/<int:habit_id>/', views.update_notes, name='update_notes'),
    
    # Analytics and Export
    path('analytics/', views.analytics, name='analytics'),
    path('export/', views.export_csv, name='export_csv'),
]
