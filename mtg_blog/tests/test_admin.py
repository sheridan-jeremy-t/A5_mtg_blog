"""Test for admin config"""

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from mtg_blog.admin import PhotoSubmissionAdmin
from mtg_blog.models import PhotoSubmission

@pytest.fixture
def admin_user():
    """Create admin user fixture"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password'
    )

@pytest.fixture
def photo_submission():
    """Create PhotoSubmission fixture"""
    image = SimpleUploadedFile('test.jpg', b'content', content_type='image/jpeg')
    return PhotoSubmission.objects.create(
        name="Test User",
        email="test@example.com",
        photo=image,
    )

@pytest.mark.django_db
class TestPhotoSubmissionAdmin:
    """Test PhotoSubmission admin configuration"""

    def test_admin_list_display(self, admin_user, photo_submission):
        """Test admin list display configuration"""
        admin = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'name' in admin.get_list_display
        assert 'email' in admin.get_list_display
        assert 'submission_date' in admin.get_list_display

    def test_admin_list_filter(self, admin_user, photo_submission):
        """Test admin list filter configuration"""
        admin = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'submission_date' in admin.get_list_filter

    def test_admin_search_field(self, admin_user, photo_submission):
        """Test admin search field configuration"""
        admin = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'name' in admin.get_search_field
        assert 'email' in admin.get_search_field

    def test_admin_readonly_fields(self, admin_user, photo_submission):
        """Test admin readonly fields configuration"""
        admin = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'submission_date' in admin.get_readonly_fields
