from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.utils import timezone


@api_view(['GET'])
def root(request):
    """
    Root endpoint - API welcome message for Android Backend
    """
    return Response({
        'message': 'Welcome to TARS Club API - Android Backend',
        'version': '1.0.0',
        'platform': 'Android',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'home': '/api/home/',
            'admin': '/admin/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'profile': '/api/auth/profile/',
            },
            'data': {
                'site_settings': '/api/site-settings/',
                'sponsors': '/api/sponsors/',
                'social_links': '/api/social-links/',
                'classes': '/api/classes/',
                'resources': '/api/resources/',
            }
        }
    })


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint that verifies:
    - API is running
    - Database connection is working
    - Returns current timestamp
    """
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'TARS Backend API - Android',
        'platform': 'Android',
        'database': 'disconnected'
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = f'error: {str(e)}'
        return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response(health_status, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_info(request):
    """
    API information endpoint
    """
    return Response({
        'name': 'TARS Club Android API',
        'version': '1.0.0',
        'platform': 'Android',
        'description': 'Backend API specifically configured for the TARS Android app',
        'endpoints': {
            'health': '/api/health/',
            'admin': '/admin/',
            'info': '/api/info/'
        }
    })


@api_view(['GET'])
def test_classes(request):
    """Test endpoint to debug class serialization"""
    import traceback
    try:
        from core.models import Class
        from core.serializers import ClassSerializer
        
        classes = Class.objects.all()
        result = {
            "count": classes.count(),
            "classes": []
        }
        
        # Try to serialize each class individually to find the problematic one
        for cls in classes:
            try:
                serialized = ClassSerializer(cls).data
                result["classes"].append({
                    "id": cls.id,
                    "title": cls.title,
                    "status": "OK",
                    "data": serialized
                })
            except Exception as e:
                result["classes"].append({
                    "id": cls.id,
                    "title": cls.title,
                    "status": "ERROR",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
        
        return Response(result)
    except Exception as e:
        return Response({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500)
