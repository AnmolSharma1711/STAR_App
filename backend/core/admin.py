from django.contrib import admin
from .models import SiteSettings, Sponsor, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['club_name', 'club_full_name', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('club_name', 'club_full_name', 'club_motto')
        }),
        ('Images', {
            'fields': ('club_logo', 'university_logo', 'hero_background')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding more than one instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'collaboration_date', 'is_active', 'order']
    list_filter = ['is_active', 'collaboration_date']
    search_fields = ['name', 'collaboration_agenda']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-collaboration_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'website')
        }),
        ('Collaboration Details', {
            'fields': ('collaboration_agenda', 'collaboration_date')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    
    fieldsets = (
        ('Link Information', {
            'fields': ('platform', 'url', 'icon_class')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )

