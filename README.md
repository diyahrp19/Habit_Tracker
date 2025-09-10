# Habit Tracker

A Django-based web application to help users build and maintain positive habits. Users can create, track, and analyze their daily habits, with features for user authentication, analytics, and habit management.

## Features

- User registration and login
- Create, edit, and delete habits
- Daily habit tracking and reset
- Analytics dashboard for habit performance
- Responsive UI with custom CSS and JavaScript

## Project Structure

```
Habit_Tracker/
├── accounts/                # User authentication views
├── habits/                  # Habit models, views, forms, management commands
│   ├── management/          # Custom Django management commands
│   └── migrations/          # Database migrations
├── habit_tracker/           # Project settings and URLs
├── static/                  # Static files (CSS, JS)
├── templates/               # HTML templates
│   ├── habits/              # Habit-related templates
│   └── registration/        # Auth templates
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Habit_Tracker
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
7. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Folder Details

- `accounts/`: Handles user authentication (login, signup)
- `habits/`: Core app for habit management, analytics, and custom commands
- `habit_tracker/`: Project configuration (settings, URLs)
- `static/`: CSS and JavaScript files
- `templates/`: HTML templates for all pages

## Custom Management Commands

- `reset_daily_habits`: Resets daily habit statuses (can be scheduled via cron or Windows Task Scheduler)

## License

This project is for educational purposes.
