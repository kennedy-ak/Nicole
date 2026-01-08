from django.db import models
from django.core.validators import FileExtensionValidator
import os


def upload_to(instance, filename):
    """Generate upload path for images"""
    return os.path.join('uploads', str(instance.id), filename)


class Submission(models.Model):
    """
    Model to store eye image submissions from participants.
    Each submission contains three images: left eye, right eye, and camera specifications.
    """
    
    # Image fields
    left_eye_image = models.ImageField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])],
        verbose_name='Left Eye Image'
    )
    
    right_eye_image = models.ImageField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])],
        verbose_name='Right Eye Image'
    )
    
    camera_specs_image = models.ImageField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])],
        verbose_name='Camera Specifications Screenshot'
    )
    
    # Camera type field
    CAMERA_CHOICES = [
        ('front', 'Front Camera'),
        ('back', 'Back Camera'),
    ]

    camera_type = models.CharField(
        max_length=10,
        choices=CAMERA_CHOICES,
        default='back',
        verbose_name='Camera Type Used',
        help_text='Which camera did you use to take the eye images?'
    )

    # Consent field
    consent = models.BooleanField(
        default=False,
        verbose_name='I consent to the use of my eye images for AI model validation'
    )

    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Submission Date')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Address')
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
    
    def __str__(self):
        return f"Submission #{self.id} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_filename(self, field_name):
        """Get the original filename from an ImageField"""
        field = getattr(self, field_name)
        if field and hasattr(field, 'name'):
            return os.path.basename(field.name)
        return None
