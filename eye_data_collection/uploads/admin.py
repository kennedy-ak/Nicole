from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
import json
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing eye image submissions.
    Includes display, filtering, search, and export functionality.
    """
    
    # Display fields in list view
    list_display = (
        'id',
        'submitted_at',
        'ip_address',
        'has_left_eye',
        'has_right_eye',
        'has_camera_specs',
    )
    
    # Add filtering capabilities
    list_filter = (
        'submitted_at',
        'ip_address',
    )
    
    # Add search functionality
    search_fields = (
        'id',
        'ip_address',
    )
    
    # Ordering
    ordering = ('-submitted_at',)
    
    # Number of items per page
    list_per_page = 25
    
    # Read-only fields
    readonly_fields = ('submitted_at', 'ip_address')
    
    # Fieldsets for better organization in detail view
    fieldsets = (
        ('Submission Information', {
            'fields': ('id', 'submitted_at', 'ip_address')
        }),
        ('Eye Images', {
            'fields': ('left_eye_image', 'right_eye_image')
        }),
        ('Camera Specifications', {
            'fields': ('camera_specs_image',)
        }),
    )
    
    # Actions for bulk operations
    actions = ['export_as_csv', 'export_as_json']
    
    def has_left_eye(self, obj):
        """Display whether left eye image exists"""
        return bool(obj.left_eye_image)
    has_left_eye.boolean = True
    has_left_eye.short_description = 'Left Eye'
    
    def has_right_eye(self, obj):
        """Display whether right eye image exists"""
        return bool(obj.right_eye_image)
    has_right_eye.boolean = True
    has_right_eye.short_description = 'Right Eye'
    
    def has_camera_specs(self, obj):
        """Display whether camera specs image exists"""
        return bool(obj.camera_specs_image)
    has_camera_specs.boolean = True
    has_camera_specs.short_description = 'Camera Specs'
    
    def export_as_csv(self, request, queryset):
        """
        Export selected submissions as CSV file.
        Each row represents one submission with all three images linked by submission ID.
        """
        response = HttpResponse(content_type='text/csv')
        filename = f'submissions_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Write header
        header = [
            'Submission ID',
            'Submitted At',
            'IP Address',
            'Left Eye Image',
            'Right Eye Image',
            'Camera Specs Image',
        ]
        writer.writerow(header)
        
        # Write data rows
        for submission in queryset:
            row = [
                submission.id,
                submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                submission.ip_address or '',
                submission.left_eye_image.name if submission.left_eye_image else '',
                submission.right_eye_image.name if submission.right_eye_image else '',
                submission.camera_specs_image.name if submission.camera_specs_image else '',
            ]
            writer.writerow(row)
        
        self.message_user(
            request,
            f'Successfully exported {queryset.count()} submission(s) as CSV.'
        )
        return response
    
    export_as_csv.short_description = 'Export selected submissions as CSV'
    
    def export_as_json(self, request, queryset):
        """
        Export selected submissions as JSON file.
        Each submission is an object with all metadata and image paths.
        """
        response = HttpResponse(content_type='application/json')
        filename = f'submissions_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Build data structure
        data = []
        for submission in queryset:
            submission_data = {
                'submission_id': submission.id,
                'submitted_at': submission.submitted_at.isoformat(),
                'ip_address': submission.ip_address,
                'images': {
                    'left_eye': submission.left_eye_image.name if submission.left_eye_image else None,
                    'right_eye': submission.right_eye_image.name if submission.right_eye_image else None,
                    'camera_specs': submission.camera_specs_image.name if submission.camera_specs_image else None,
                }
            }
            data.append(submission_data)
        
        # Write JSON
        json.dump(data, response, indent=2)
        
        self.message_user(
            request,
            f'Successfully exported {queryset.count()} submission(s) as JSON.'
        )
        return response
    
    export_as_json.short_description = 'Export selected submissions as JSON'
