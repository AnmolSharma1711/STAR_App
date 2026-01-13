# Quick start script for TARS backend (Windows)

Write-Host "🚀 Starting TARS Backend Server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will be accessible at:" -ForegroundColor Cyan
Write-Host "  - http://localhost:8000 (local)" -ForegroundColor Yellow
Write-Host "  - http://192.168.198.127:8000 (network)" -ForegroundColor Yellow
Write-Host "  - http://192.168.56.1:8000 (network)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

# Run migrations
python manage.py migrate

# Start server on all interfaces
python manage.py runserver 0.0.0.0:8000
