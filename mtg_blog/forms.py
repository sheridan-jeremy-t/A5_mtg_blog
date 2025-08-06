"""Blog forms"""
from django import forms
from .models import PhotoSubmission

class PhotoSubmissionForm(forms.ModelForm):
    """Form for Photo Submission"""
    class Meta:
        """Meta options for PhotoSubmissionForm"""
        model = PhotoSubmission
        fields = ['name', 'email', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def clean_photo(self):
        """Validate photo upload"""
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 5 * 1024 * 1024: #makes a 5MB limit
                raise forms.ValidationError("Image file too large (5MB limit)")
            if not photo.content_type.startswith('image/'):
                raise forms.ValidationError("Image file must be an image file")
        return photo