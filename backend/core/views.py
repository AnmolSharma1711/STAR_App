from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import models
from .models import SiteSettings, Sponsor, SocialLink, Class, Resource, TeamMember, Domain, Member, Meeting
from .serializers import (
    SiteSettingsSerializer, SponsorSerializer, SocialLinkSerializer,
    ClassSerializer, ResourceSerializer, TeamMemberSerializer,
    DomainSerializer, MemberSerializer, MeetingSerializer
)


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for site settings"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for sponsors"""
    queryset = Sponsor.objects.filter(is_active=True)
    serializer_class = SponsorSerializer
    permission_classes = [AllowAny]


class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for social links"""
    queryset = SocialLink.objects.filter(is_active=True)
    serializer_class = SocialLinkSerializer
    permission_classes = [AllowAny]


class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for classes - requires authentication"""
    queryset = Class.objects.filter(is_active=True)
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for resources - requires authentication"""
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for mentors/leads"""
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]


class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for member domains"""
    queryset = Domain.objects.filter(is_active=True)
    serializer_class = DomainSerializer
    permission_classes = [AllowAny]


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for members (PII)"""
    queryset = Member.objects.filter(is_active=True)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self.request.user, 'is_staff', False):
            return Member.objects.filter(is_active=True).select_related('user', 'domain', 'lead')
        return Member.objects.filter(is_active=True, user=self.request.user).select_related('user', 'domain', 'lead')


class MeetingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for meetings.
    - Team members (admin/lead/mentor) can create, update, delete meetings
    - Regular members can only view meetings (filtered by their domain or all if no domain restriction)
    """
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()  # Required for router.register()
    
    def get_queryset(self):
        """
        Filter meetings based on user role:
        - Admins/Staff: see all meetings
        - Team members (lead/mentor): see all meetings
        - Regular members: see meetings for their domain or meetings marked for all domains
        """
        user = self.request.user
        
        # Get all active meetings
        meetings = Meeting.objects.filter(is_active=True).prefetch_related('domains', 'speaker', 'scheduled_by')
        
        # If user is staff/admin, return all meetings
        if user.is_staff:
            return meetings
        
        # Check if user is a team member (lead/mentor/admin via TeamMember)
        try:
            team_member = user.team_member_profile
            # Team members see all meetings
            return meetings
        except:
            pass
        
        # Regular member: filter by domain
        try:
            member = user.member_profile
            if member.domain:
                # Show meetings for their domain OR meetings for all domains (no domains selected)
                # A meeting with no domains means it's for everyone
                meetings_for_domain = meetings.filter(domains__id=member.domain.id)
                meetings_for_all = meetings.filter(domains__isnull=True)
                # Also include meetings where domains field is empty (ManyToMany empty means for all)
                meetings_with_no_domains = meetings.annotate(
                    domain_count=models.Count('domains')
                ).filter(domain_count=0)
                return (meetings_for_domain | meetings_for_all | meetings_with_no_domains).distinct()
            else:
                # No domain assigned, show only all-domains meetings
                meetings_with_no_domains = meetings.annotate(
                    domain_count=models.Count('domains')
                ).filter(domain_count=0)
                return meetings_with_no_domains.distinct()
        except:
            # User has no member profile, don't show any meetings
            return meetings.none()
    
    def create(self, request, *args, **kwargs):
        """Only team members can create meetings"""
        user = request.user
        
        # Check if user is staff or team member
        if not user.is_staff:
            try:
                team_member = user.team_member_profile
            except:
                return Response(
                    {'detail': 'Only team members (leads/mentors) can schedule meetings'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Only the creator or staff can update meetings"""
        meeting = self.get_object()
        user = request.user
        
        if not user.is_staff and meeting.scheduled_by.user != user:
            return Response(
                {'detail': 'You can only update meetings you created'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only the creator or staff can delete meetings"""
        meeting = self.get_object()
        user = request.user
        
        if not user.is_staff and meeting.scheduled_by.user != user:
            return Response(
                {'detail': 'You can only delete meetings you created'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my_scheduled(self, request):
        """Get meetings scheduled by the current user"""
        user = request.user
        
        try:
            team_member = user.team_member_profile
            meetings = Meeting.objects.filter(scheduled_by=team_member, is_active=True)
            serializer = self.get_serializer(meetings, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {'detail': 'You are not a team member'},
                status=status.HTTP_403_FORBIDDEN
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def home_page_data(request):
    """
    Single endpoint to get all home page data
    """
    # Get site settings (should be only one)
    site_settings = SiteSettings.objects.first()
    
    # Get active sponsors
    sponsors = Sponsor.objects.filter(is_active=True)

    # Get active mentors/leads
    mentors = TeamMember.objects.filter(is_active=True, role='mentor')
    leads = TeamMember.objects.filter(is_active=True, role='lead')
    
    # Get active social links
    social_links = SocialLink.objects.filter(is_active=True)
    
    return Response({
        'site_settings': SiteSettingsSerializer(site_settings).data if site_settings else None,
        'sponsors': SponsorSerializer(sponsors, many=True).data,
        'mentors': TeamMemberSerializer(mentors, many=True).data,
        'leads': TeamMemberSerializer(leads, many=True).data,
        'social_links': SocialLinkSerializer(social_links, many=True).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_portal_data(request):
    """
    Single endpoint to get all member portal data
    """
    # Get active classes
    classes = Class.objects.filter(is_active=True)
    
    # Get active resources
    resources = Resource.objects.filter(is_active=True)
    
    return Response({
        'classes': ClassSerializer(classes, many=True).data,
        'resources': ResourceSerializer(resources, many=True).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_download(request, resource_id):
    """
    Increment download count for a resource
    """
    try:
        resource = Resource.objects.get(id=resource_id, is_active=True)
        resource.download_count += 1
        resource.save(update_fields=['download_count'])
        return Response({
            'success': True,
            'download_count': resource.download_count
        })
    except Resource.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Resource not found'
        }, status=status.HTTP_404_NOT_FOUND)

