from django import forms
from django.core.validators import FileExtensionValidator
from .models import Submission


class SubmissionForm(forms.ModelForm):
    """
    Form for uploading eye images.
    Validates file types and sizes.
    """
    
    # Maximum file size: 10MB
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    consent = forms.BooleanField(
        label='I consent to the use of my eye images for AI model validation',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'You must consent to submit your images.'}
    )
    
    class Meta:
        model = Submission
        fields = ['left_eye_image', 'right_eye_image', 'camera_specs_image', 'consent']
        widgets = {
            'left_eye_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/heic'
            }),
            'right_eye_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/heic'
            }),
            'camera_specs_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png'
            }),
        }
        labels = {
            'left_eye_image': 'Upload Image of Your Left Eye (Taken with your smartphone)',
            'right_eye_image': 'Upload Image of Your Right Eye (Taken with your smartphone)',
            'camera_specs_image': 'Upload Screenshot of Your Smartphone Camera Specifications',
        }
        help_texts = {
            'left_eye_image': 'Accepted formats: JPG, JPEG, PNG, HEIC. Maximum size: 10MB.',
            'right_eye_image': 'Accepted formats: JPG, JPEG, PNG, HEIC. Maximum size: 10MB.',
            'camera_specs_image': 'Accepted formats: JPG, JPEG, PNG. Maximum size: 10MB.',
        }
    
    def clean_left_eye_image(self):
        image = self.cleaned_data.get('left_eye_image')
        if image:
            self._validate_file_size(image)
        return image
    
    def clean_right_eye_image(self):
        image = self.cleaned_data.get('right_eye_image')
        if image:
            self._validate_file_size(image)
        return image
    
    def clean_camera_specs_image(self):
        image = self.cleaned_data.get('camera_specs_image')
        if image:
            self._validate_file_size(image)
        return image
    
    def _validate_file_size(self, file):
        """Validate that file size does not exceed maximum"""
        if file.size > self.MAX_FILE_SIZE:
            raise forms.ValidationError(
                f'File size exceeds maximum limit of {self.MAX_FILE_SIZE // (1024*1024)}MB. '
                f'Your file is {file.size // (1024*1024)}MB.'
            )
