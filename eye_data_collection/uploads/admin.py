from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
import json
import zipfile
import os
from io import BytesIO
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
    readonly_fields = ('id', 'submitted_at', 'ip_address')
    
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
    actions = ['export_as_csv', 'export_as_json', 'export_as_zip']
    
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

    def export_as_zip(self, request, queryset):
        """
        Export selected submissions as ZIP file containing all images and a CSV manifest.
        The ZIP file structure:
        - submissions_manifest.csv (metadata for all submissions)
        - left_eye/ (folder with all left eye images)
        - right_eye/ (folder with all right eye images)
        - camera_specs/ (folder with all camera specs images)
        """
        # Create in-memory ZIP file
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Create CSV manifest
            csv_buffer = BytesIO()
            csv_writer = csv.writer(csv_buffer.io.TextIOWrapper(encoding='utf-8'))

            # Write CSV header
            header = [
                'Submission ID',
                'Submitted At',
                'IP Address',
                'Camera Type',
                'Left Eye Image Filename',
                'Right Eye Image Filename',
                'Camera Specs Image Filename',
            ]
            csv_writer.writerow(header)

            # Process each submission
            for submission in queryset:
                # Write CSV row
                row = [
                    submission.id,
                    submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                    submission.ip_address or '',
                    submission.get_camera_type_display() if submission.camera_type else '',
                    f'left_eye/submission_{submission.id}_{os.path.basename(submission.left_eye_image.name)}' if submission.left_eye_image else '',
                    f'right_eye/submission_{submission.id}_{os.path.basename(submission.right_eye_image.name)}' if submission.right_eye_image else '',
                    f'camera_specs/submission_{submission.id}_{os.path.basename(submission.camera_specs_image.name)}' if submission.camera_specs_image else '',
                ]
                csv_writer.writerow(row)

                # Add left eye image to ZIP
                if submission.left_eye_image:
                    try:
                        image_path = f'left_eye/submission_{submission.id}_{os.path.basename(submission.left_eye_image.name)}'
                        zip_file.writestr(image_path, submission.left_eye_image.read())
                    except Exception as e:
                        pass  # Skip if file can't be read

                # Add right eye image to ZIP
                if submission.right_eye_image:
                    try:
                        image_path = f'right_eye/submission_{submission.id}_{os.path.basename(submission.right_eye_image.name)}'
                        zip_file.writestr(image_path, submission.right_eye_image.read())
                    except Exception as e:
                        pass  # Skip if file can't be read

                # Add camera specs image to ZIP
                if submission.camera_specs_image:
                    try:
                        image_path = f'camera_specs/submission_{submission.id}_{os.path.basename(submission.camera_specs_image.name)}'
                        zip_file.writestr(image_path, submission.camera_specs_image.read())
                    except Exception as e:
                        pass  # Skip if file can't be read

            # Add CSV manifest to ZIP
            csv_buffer.seek(0)
            zip_file.writestr('submissions_manifest.csv', csv_buffer.read())

        # Prepare response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        filename = f'submissions_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.zip'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        self.message_user(
            request,
            f'Successfully exported {queryset.count()} submission(s) with images as ZIP.'
        )
        return response

    export_as_zip.short_description = 'Export selected submissions with images as ZIP'
