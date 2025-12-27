from rest_framework import serializers
from .models import SiteSettings, Sponsor, SocialLink


class SiteSettingsSerializer(serializers.ModelSerializer):
    club_logo = serializers.SerializerMethodField()
    university_logo = serializers.SerializerMethodField()
    hero_background = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSettings
        fields = ['id', 'club_name', 'club_full_name', 'club_motto', 'club_logo', 'university_logo', 'hero_background', 'updated_at']
    
    def get_club_logo(self, obj):
        if obj.club_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.club_logo.url)
            return obj.club_logo.url
        return None
    
    def get_university_logo(self, obj):
        if obj.university_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.university_logo.url)
            return obj.university_logo.url
        return None
    
    def get_hero_background(self, obj):
        if obj.hero_background:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_background.url)
            return obj.hero_background.url
        return None


class SponsorSerializer(serializers.ModelSerializer):
    collaboration_date_formatted = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Sponsor
        fields = [
            'id', 'name', 'logo', 'website', 'collaboration_agenda', 
            'collaboration_date', 'collaboration_date_formatted', 'is_active', 'order'
        ]
    
    def get_collaboration_date_formatted(self, obj):
        return obj.collaboration_date.strftime('%B %Y')
    
    def get_logo(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_display', 'url', 'icon_class', 'is_active', 'order']
