import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mtg_blog.models import Post, Topic
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils import timezone
from mtg_blog.models import PhotoSubmission
from mtg_blog.tests.test_admin import sample_photo_submission


class TestTopicModel(TestCase):
    """Test the topic model"""
    def test_topic_creation(self):
        """Test Topic model with the required fields"""
        topic = Topic.objects.create(
            name="Standard",
            slug="standard"
        )
        self.assertEqual(topic.name, "Standard")
        self.assertEqual(topic.slug, "standard")
        self.assertEqual(str(topic), "Standard")
    def test_topic_unique_name(self):
        """Test that topic has a unique name"""
        Topic.objects.create(name="Commander", slug="commander")
        with self.assertRaises(ValidationError):
            topic = Topic(name="Commander", slug="commander-edh")
            topic.full_clean()

class TestPostModel(TestCase):
    """Test the Post Model"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='mtgpro',
            email='mtgpro@example.com',
            password='planeswalker123'
        )
        self.topic = Topic.objects.create(
            name = 'Deck Tech',
            slug = 'deck-tech'
        )
    def test_post_creation(self):
        """Test Post model creation"""
        post = Post.objects.create(
            title = 'Best Blue Control Deck in Standard',
            content = 'This control deck dominates the current meta',
            author = self.user,
            status = 'draft',
            slug = 'best-blue-control-deck-standard'
        )
        self.assertEqual(post.title, "Best Blue Control Deck in Standard")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 'draft')
        self.assertIsNotNone(post.created)
        self.assertIsNotNone(post.updated)
    def test_post_default_status(self):
        """Test that default status is draft"""
        post = Post.objects.create(
            title = 'Modern Burn Deck Guide',
            author = self.user,
            slug = 'modern-burn-guide'
        )
        self.assertEqual(post.status, 'draft')
    def test_post_published_timestamp(self):
        """Test published timestamp is set when status changes to published"""
        post = Post.objects.create(
            title = "Pioneer Deck Breakdown",
            author = self.user,
            slug = 'pioneer-deck-breakdown',
            status = 'published'
        )
        self.assertIsNotNone(post.published)

@pytest.mark.django_db
def test_topic_get_absolute_url():
    """Test the absolute topic url"""
    topic = Topic.objects.create(name = 'Red Aggro', slug='red-aggro')
    expected_url = '/topic/red-aggro'
    assert topic.get_absolute_url() == expected_url

@pytest.mark.django_db
class TestPhotoSubmissionModel:
    """Test PhotoSubmission model."""

    def test_photo_submission_creation(self):
        """Test photo submission creation."""
        # create a test image
        test_image = SimpleUploadedFile("test.jpg", b"fake_image_content", content_type="image/jpeg")
        photo_submission = PhotoSubmission.objects.create(
            name="Test User",
            email="test@example.com",
            photo=test_image
        )
        assert photo_submission.name == "Test User"
        assert photo_submission.email == "test@example.com"
        assert photo_submission.photo.name.startswith("contest_photos/")
        assert photo_submission.submission_date is not None

    def test_photo_submission_str_method(self):
        """Test string representation of PhotoSubmission."""
        test_image = SimpleUploadedFile(
            "test.jpg",
            b"fake_image_content",
            content_type="image/jpeg"
        )
        photo_submission = PhotoSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            photo=test_image
        )
        expected_str = f"Photo Submission by John Doe on {photo_submission.submission_date.strftime('%Y-%m-%d')}"
        assert str(photo_submission) == expected_str

    def test_model_fields(self):
        """Test model fields properties."""
        model_fields = PhotoSubmission._meta.get_fields()
        field_names = [field.name for field in model_fields]

        assert 'name' in field_names
        assert 'email' in field_names
        assert 'photo' in field_names
        assert 'submission_date' in field_names

    def test_name_max_length(self):
        """Test model field name max length."""
        name_field = PhotoSubmission._meta.get_field('name')
        assert name_field.max_length == 100

    def test_email_field_type(self):
        """Test model field email type."""
        email_field = PhotoSubmission._meta.get_field('email')
        assert isinstance(email_field, models.EmailField)
