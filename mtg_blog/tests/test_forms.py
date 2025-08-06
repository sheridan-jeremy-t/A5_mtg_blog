"""Tests for PhotoSubmissionForm."""
import pytest
from django.core.files.uploadedfile import SimpleUploadeFile, SimpleUploadedFile
from mtg_blog.forms import PhotoSubmissionForm

class TestPhotoSubmissionForm:
    """Tests for PhotoSubmissionForm."""

    def test_form_valid_data(self):
        image = SimpleUploadedFile(
            'test.jpg',
            b'file_content',
            content_type='image/jpeg'
        )

        form_data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
        }
        form_files = {
            'photo' : image,
        }
        form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert form.is_valid()

    def test_form_missing_name(self):
        """Test form validation with missing name."""
        image = SimpleUploadedFile("test.jpg", b'content', content_type='image/jpeg')
        form_data = {
            'email' : 'test@example.com',
        }

        form_files = {
            'photo' : image,
        }

        form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert not form.is_valid()
        assert 'name' in form.errors

    def test_form_invaild_email(self):
        """Test form validation with invalid email."""
        image = SimpleUploadedFile("test.jpg", b'content', content_type='image/jpeg')

        form_data = {
            'name' : 'Test User',
            'email' : 'invalid email',
        }

        form_files = {
            'photo' : image,
        }

        form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_form_missing_photo(self):
        """Test form validation with missing photo."""
        form_data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
        }

        form = PhotoSubmissionForm(data=form_data)
        assert not form.is_valid()
        assert 'photo' in form.errors