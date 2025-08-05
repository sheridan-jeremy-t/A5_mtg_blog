import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mtg_blog.models import Post, Topic

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
