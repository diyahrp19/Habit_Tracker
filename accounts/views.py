from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm

# display signup form and create new user
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('habits:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
# simple profile page for logged-in users
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
