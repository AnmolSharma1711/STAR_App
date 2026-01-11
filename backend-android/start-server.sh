#!/bin/bash

# Start script for Android backend

echo "🤖 Starting TARS Android Backend Server..."

# Run migrations
python manage.py migrate --noinput

# Start server with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 tars.wsgi:application
