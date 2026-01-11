#!/bin/bash

# Build script for Android backend deployment

echo "🚀 Starting Android Backend Deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations (connects to shared database)
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"
echo "💡 To start the server, run: gunicorn --bind 0.0.0.0:8000 tars.wsgi:application"
