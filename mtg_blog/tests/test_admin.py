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
def sample_photo_submission():
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

    def test_admin_list_display(self, admin_user, sample_photo_submission):
        """Test admin list display configuration"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'name' in admin_instance.list_display
        assert 'email' in admin_instance.list_display
        assert 'submission_date' in admin_instance.list_display

    def test_admin_list_filter(self, admin_user, sample_photo_submission):
        """Test admin list filter configuration"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'submission_date' in admin_instance.list_filter

    def test_admin_search_fields(self, admin_user, sample_photo_submission):
        """Test admin search field configuration"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'name' in admin_instance.search_fields
        assert 'email' in admin_instance.search_fields

    def test_admin_readonly_fields(self, admin_user, sample_photo_submission):
        """Test admin readonly fields configuration"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert 'submission_date' in admin_instance.readonly_fields

    def test_admin_ordering(self, admin_user, sample_photo_submission):
        """Test admin ordering configuration"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())
        assert admin_instance.ordering == ['-submission_date']

    def test_admin_photo_thumbnail_method(self, admin_user, sample_photo_submission):
        """Test photo thumbnail method exists"""
        admin_instance = PhotoSubmissionAdmin(PhotoSubmission, AdminSite())

        assert hasattr(admin_instance, 'photo_thumbnail')
        assert callable(admin_instance.photo_thumbnail)

        thumbnail_html = admin_instance.photo_thumbnail(sample_photo_submission)
        assert 'img src=' in thumbnail_html
        assert 'width="50"' in thumbnail_html
