#!/bin/bash
# Quick start script for TARS backend

echo "🚀 Starting TARS Backend Server..."
echo ""
echo "Server will be accessible at:"
echo "  - http://localhost:8000 (local)"
echo "  - http://192.168.198.127:8000 (network)"
echo "  - http://192.168.56.1:8000 (network)"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run migrations
python manage.py migrate

# Start server on all interfaces
python manage.py runserver 0.0.0.0:8000
