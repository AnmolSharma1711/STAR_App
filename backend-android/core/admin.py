from django.contrib import admin
from .models import SiteSettings, Sponsor, SocialLink, Class, Resource, TeamMember, Domain, Member


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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'position', 'user', 'is_active', 'order']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'position', 'email']
    list_editable = ['is_active', 'order']
    ordering = ['role', 'order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'role', 'position', 'image')
        }),
        ('Details', {
            'fields': ('quote', 'tech_stack', 'email')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url', 'instagram_url', 'website_url')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'display_name']
    list_editable = ['is_active']
    ordering = ['display_name', 'name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'domain', 'lead', 'university_roll', 'is_active']
    list_filter = ['is_active', 'domain']
    search_fields = ['user__username', 'user__email', 'personal_mail', 'gla_mail', 'university_roll']
    ordering = ['-created_at']

    fieldsets = (
        ('Account', {
            'fields': ('user', 'is_active')
        }),
        ('Club', {
            'fields': ('domain', 'lead', 'university_roll')
        }),
        ('Contact', {
            'fields': ('phone_number', 'personal_mail', 'gla_mail')
        }),
        ('Social', {
            'fields': ('linkedin_url', 'github_url')
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


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'difficulty', 'status', 'is_active']
    list_filter = ['difficulty', 'status', 'is_active']
    search_fields = ['title', 'instructor', 'description']
    list_editable = ['is_active']
    ordering = ['-id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor', 'thumbnail')
        }),
        ('Class Details', {
            'fields': ('difficulty', 'status', 'duration', 'start_date', 'end_date')
        }),
        ('Enrollment', {
            'fields': ('max_participants', 'enrolled_count')
        }),
        ('Location & Links', {
            'fields': ('location', 'meeting_link', 'syllabus')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'download_count', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'author', 'tags']
    list_editable = ['is_featured', 'is_active']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'author', 'thumbnail')
        }),
        ('Content', {
            'fields': ('file', 'external_link')
        }),
        ('Metadata', {
            'fields': ('tags', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('download_count',),
            'description': 'Download count updates automatically when users download resources.'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'download_count']
