@echo off
REM Batch start script for Android backend (Windows)

echo 🤖 Starting TARS Android Backend Server...

REM Run migrations
echo Running database migrations...
python manage.py migrate --noinput

REM Start development server
echo Starting Django development server on port 8001...
python manage.py runserver 0.0.0.0:8001

pause
