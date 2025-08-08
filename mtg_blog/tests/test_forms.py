"""Tests for PhotoSubmissionForm."""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from mtg_blog.forms import PhotoSubmissionForm

class TestPhotoSubmissionForm:
    """Tests for PhotoSubmissionForm."""

    def test_form_valid_data(self):
        test_image = SimpleUploadedFile(
            'test.jpg',
            b'fake_image_content',
            content_type='image/jpeg'
        )

        form_data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
        }
        form_files = {
            'photo' : test_image,
        }
        test_form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert test_form.is_valid()

    def test_form_missing_name(self):
        """Test form validation with missing name."""
        test_image = SimpleUploadedFile("test.jpg", b'fake_image_content', content_type='image/jpeg')
        form_data = {
            'email' : 'test@example.com',
        }

        form_files = {
            'photo' : test_image,
        }

        test_form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert not test_form.is_valid()
        assert 'name' in test_form.errors

    def test_form_invalid_email(self):
        """Test form validation with invalid email."""
        test_image = SimpleUploadedFile("test.jpg", b'content', content_type='image/jpeg')

        form_data = {
            'name' : 'Test User',
            'email' : 'invalid email',
        }

        form_files = {
            'photo' : test_image,
        }

        test_form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert not test_form.is_valid()
        assert 'email' in test_form.errors

    def test_form_missing_photo(self):
        """Test form validation with missing photo."""
        form_data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
        }

        test_form = PhotoSubmissionForm(data=form_data)
        assert not test_form.is_valid()
        assert 'photo' in test_form.errors

    def test_form_file_size_validation(self):
        """Test form validation with file size."""
        #create a file to large
        large_test_image = SimpleUploadedFile(
            'large_test_image.jgp',
            b"x" * (6 * 1024 * 1024), #6MB file
            content_type='image/jpeg'
        )

        form_data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
        }
        form_files = {'photo' : large_test_image}

        test_form = PhotoSubmissionForm(data=form_data, files=form_files)
        assert not test_form.is_valid()
        assert 'photo' in test_form.errors