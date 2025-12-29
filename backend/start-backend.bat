@echo off
echo ========================================
echo Starting TARS Backend Server
echo ========================================
echo.
echo Server will be accessible at:
echo   - http://localhost:8000 (local computer)
echo   - http://192.168.198.127:8000 (from other devices)
echo   - http://192.168.56.1:8000 (from other devices)
echo.
echo CORS is configured for:
echo   - All localhost ports
echo   - All local network IPs
echo   - Capacitor/Ionic apps
echo   - Production domains
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python manage.py runserver 0.0.0.0:8000
