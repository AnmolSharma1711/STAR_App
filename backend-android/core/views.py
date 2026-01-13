from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import SiteSettings, Sponsor, SocialLink, Class, Resource, TeamMember, Domain, Member
from .serializers import (
    SiteSettingsSerializer, SponsorSerializer, SocialLinkSerializer,
    ClassSerializer, ResourceSerializer, TeamMemberSerializer,
    DomainSerializer, MemberSerializer
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

