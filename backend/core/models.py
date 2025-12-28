from django.db import models
from django.core.validators import URLValidator


class SiteSettings(models.Model):
    """Site-wide settings like club name, logo, motto, etc."""
    club_name = models.CharField(max_length=200, default="TARS")
    club_full_name = models.CharField(
        max_length=500, 
        default="Technology and Automation Research Society"
    )
    club_motto = models.TextField(
        default="Pioneering the future of intelligent systems and automated solutions. "
                "Innovating at the intersection of technology, research, and human advancement."
    )
    club_logo = models.ImageField(upload_to='club/', blank=True, null=True)
    university_logo = models.ImageField(upload_to='university/', blank=True, null=True)
    hero_background = models.ImageField(upload_to='hero/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Site Settings - {self.club_name}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one SiteSettings instance is allowed')
        return super().save(*args, **kwargs)


class Sponsor(models.Model):
    """Sponsors/Partners of the club"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True, null=True, validators=[URLValidator()])
    collaboration_agenda = models.TextField(
        help_text="Purpose or agenda of collaboration"
    )
    collaboration_date = models.DateField(
        help_text="Date when collaboration started"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-collaboration_date']
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """Social media links for the club"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]
    
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(validators=[URLValidator()])
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="CSS class for icon (e.g., 'fab fa-facebook')"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"


class Class(models.Model):
    """Classes/Workshops offered by the club"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    instructor = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    thumbnail = models.ImageField(upload_to='classes/', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=100, help_text="e.g., '4 weeks' or '10 hours'")
    max_participants = models.IntegerField(default=30)
    enrolled_count = models.IntegerField(default=0)
    meeting_link = models.URLField(blank=True, null=True, help_text="Zoom/Meet link for online classes")
    location = models.CharField(max_length=300, blank=True, null=True, help_text="Physical location if applicable")
    syllabus = models.FileField(upload_to='class_syllabus/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = "Class"
        verbose_name_plural = "Classes"
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    @property
    def is_full(self):
        return self.enrolled_count >= self.max_participants


class Resource(models.Model):
    """Learning resources and materials"""
    CATEGORY_CHOICES = [
        ('tutorial', 'Tutorial'),
        ('documentation', 'Documentation'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('book', 'Book'),
        ('tool', 'Tool'),
        ('project', 'Project'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to='resources/', blank=True, null=True)
    file = models.FileField(upload_to='resource_files/', blank=True, null=True, help_text="Upload file if applicable")
    external_link = models.URLField(blank=True, null=True, help_text="External URL if applicable")
    author = models.CharField(max_length=200, blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
