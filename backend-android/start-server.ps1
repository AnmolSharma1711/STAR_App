# PowerShell start script for Android backend (Windows)

Write-Host "🤖 Starting TARS Android Backend Server..." -ForegroundColor Green

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
python manage.py migrate --noinput

# Start development server
Write-Host "Starting Django development server..." -ForegroundColor Cyan
python manage.py runserver 0.0.0.0:8001
