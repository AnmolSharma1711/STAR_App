# Generated migration to handle Class.instructor change and update Meeting model

from django.db import migrations, models
import django.db.models.deletion


def migrate_instructor_to_name(apps, schema_editor):
    """Copy existing instructor CharField values to instructor_name before converting instructor to FK"""
    Class = apps.get_model('core', 'Class')
    for cls in Class.objects.all():
        if cls.instructor:
            # Store old text value in instructor_name
            cls.instructor_name = cls.instructor
            cls.save(update_fields=['instructor_name'])


def reverse_migrate_instructor(apps, schema_editor):
    """Reverse migration - copy instructor_name back to instructor as text"""
    pass  # Not needed since we're changing field type


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_domain_teammember_user_member'),
    ]

    operations = [
        # Step 1: Add instructor_name field to store text values
        migrations.AddField(
            model_name='class',
            name='instructor_name',
            field=models.CharField(
                blank=True,
                help_text="Name of instructor if not a team member (for 'Other' option)",
                max_length=200,
                null=True,
            ),
        ),
        # Step 2: Run data migration to copy instructor text to instructor_name
        migrations.RunPython(migrate_instructor_to_name, reverse_migrate_instructor),
        # Step 3: Remove old instructor CharField
        migrations.RemoveField(
            model_name='class',
            name='instructor',
        ),
        # Step 4: Add new instructor ForeignKey field
        migrations.AddField(
            model_name='class',
            name='instructor',
            field=models.ForeignKey(
                blank=True,
                help_text="Instructor from team members. If not set, use instructor_name field.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='classes_taught',
                to='core.teammember',
            ),
        ),
        
        # ==================== MEETING MODEL UPDATES ====================
        # First, drop the old Meeting table and recreate with new structure
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS core_meeting_domains CASCADE;',
            reverse_sql='',  # No reverse needed
        ),
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS core_meeting CASCADE;',
            reverse_sql='',  # No reverse needed
        ),
        
        # Step 5: Create Meeting model with new structure
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Meeting title/topic', max_length=300)),
                ('description', models.TextField(blank=True, help_text='Meeting agenda and details', null=True)),
                ('speaker_other', models.CharField(blank=True, help_text='Name of speaker if not a team member (e.g., guest speaker)', max_length=200, null=True)),
                ('scheduled_date', models.DateTimeField(help_text='When the meeting is scheduled')),
                ('end_time', models.DateTimeField(blank=True, help_text='When the meeting ends', null=True)),
                ('meeting_link', models.URLField(blank=True, help_text='Zoom/Google Meet/Teams link', null=True)),
                ('location', models.CharField(blank=True, help_text='Physical location if in-person', max_length=300, null=True)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='upcoming', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('domains', models.ManyToManyField(blank=True, help_text='Select domains who can see this meeting. Leave empty to make visible to all.', related_name='meetings', to='core.domain')),
                ('scheduled_by', models.ForeignKey(help_text='Team member (admin/lead/mentor) who scheduled this meeting', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetings_scheduled', to='core.teammember')),
                ('speaker', models.ForeignKey(blank=True, help_text='Speaker/Presenter if from team members', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetings_led', to='core.teammember')),
            ],
            options={
                'verbose_name': 'Meeting',
                'verbose_name_plural': 'Meetings',
                'ordering': ['-scheduled_date'],
            },
        ),
    ]
