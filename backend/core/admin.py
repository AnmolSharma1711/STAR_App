from django.contrib import admin
from .models import SiteSettings, Sponsor, SocialLink, Class, Resource, TeamMember, Domain, Member, Meeting


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
    list_display = ['title', 'instructor_display', 'difficulty', 'status', 'start_date', 'enrolled_count', 'max_participants', 'is_active']
    list_filter = ['difficulty', 'status', 'is_active', 'start_date']
    search_fields = ['title', 'instructor__name', 'instructor_name', 'description']
    list_editable = ['is_active', 'status']
    ordering = ['order', '-start_date']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'thumbnail')
        }),
        ('Instructor', {
            'fields': ('instructor', 'instructor_name'),
            'description': 'Select instructor from team members, or leave empty and fill instructor_name for external instructors.'
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
    
    def instructor_display(self, obj):
        if obj.instructor:
            return obj.instructor.name
        return obj.instructor_name or "Unknown"
    instructor_display.short_description = 'Instructor'


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


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker_display', 'scheduled_date', 'status', 'domain_list', 'scheduled_by_display', 'is_active']
    list_filter = ['status', 'is_active', 'domains', 'scheduled_date']
    search_fields = ['title', 'description', 'speaker__name', 'speaker_other', 'scheduled_by__name']
    list_editable = ['is_active', 'status']
    ordering = ['-scheduled_date']
    date_hierarchy = 'scheduled_date'
    filter_horizontal = ['domains']
    
    fieldsets = (
        ('Meeting Information', {
            'fields': ('title', 'description')
        }),
        ('Speaker', {
            'fields': ('speaker', 'speaker_other'),
            'description': 'Select speaker from team members, or leave empty and fill speaker_other for guest speakers.'
        }),
        ('Scheduling', {
            'fields': ('scheduled_by', 'scheduled_date', 'end_time')
        }),
        ('Visibility', {
            'fields': ('domains',),
            'description': 'Select which domains can see this meeting. Leave empty to make it visible to all members.'
        }),
        ('Location & Links', {
            'fields': ('meeting_link', 'location')
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def speaker_display(self, obj):
        if obj.speaker:
            return obj.speaker.name
        return obj.speaker_other or "Unknown"
    speaker_display.short_description = 'Speaker'
    
    def scheduled_by_display(self, obj):
        if obj.scheduled_by:
            return obj.scheduled_by.name
        return "Unknown"
    scheduled_by_display.short_description = 'Scheduled By'
    
    def domain_list(self, obj):
        if obj.is_for_all_domains:
            return "All Domains"
        domains = obj.domains.all()
        return ", ".join([d.display_name for d in domains]) if domains.exists() else "None"
    domain_list.short_description = 'Domains'

