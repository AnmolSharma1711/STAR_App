"""
URL configuration for tars project - Android Backend

This backend is specifically configured for the Android app.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from . import auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import (
    SiteSettingsViewSet, SponsorViewSet, SocialLinkViewSet,
    ClassViewSet, ResourceViewSet, TeamMemberViewSet, DomainViewSet, MemberViewSet, home_page_data, member_portal_data,
    increment_download
)

# Create router for viewsets
router = DefaultRouter()
router.register(r'site-settings', SiteSettingsViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'social-links', SocialLinkViewSet)
router.register(r'team-members', TeamMemberViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'members', MemberViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'resources', ResourceViewSet)

# Customize admin site headers
admin.site.site_header = "TARS Club Administration (Android Backend)"
admin.site.site_title = "TARS Android Admin Portal"
admin.site.index_title = "Welcome to TARS Club Management - Android Backend"

urlpatterns = [
    # Root endpoint
    path("", views.root, name="root"),
    
    # Admin
    path("admin/", admin.site.urls),
    
    # Health & Info
    path("api/health/", views.health_check, name="health_check"),
    path("api/info/", views.api_info, name="api_info"),
    
    # Home page data
    path("api/home/", home_page_data, name="home_page_data"),
    
    # Member portal data
    path("api/portal/", member_portal_data, name="member_portal_data"),
    
    # Increment download count
    path("api/resources/<int:resource_id>/download/", increment_download, name="increment_download"),
    
    # API router (includes site-settings, sponsors, social-links, classes, resources)
    path("api/", include(router.urls)),
    
    # Authentication
    path("api/auth/register/", auth_views.register, name="register"),
    path("api/auth/login/", auth_views.login, name="login"),
    path("api/auth/logout/", auth_views.logout, name="logout"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # User Profile
    path("api/auth/profile/", auth_views.user_profile, name="user_profile"),
    path("api/auth/profile/update/", auth_views.update_profile, name="update_profile"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
