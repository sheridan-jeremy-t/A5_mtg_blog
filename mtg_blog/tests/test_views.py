"""Test Views"""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from mtg_blog.models import Topic, Post, PhotoSubmission

@pytest.mark.django_db
def test_home_view_renders_topic(client):
    """Test the home view renders"""
    user = User.objects.create_user(username='testuser', password='pass')
    topic1 = Topic.objects.create(name='Red Aggro')
    post = Post.objects.create(
        title='Fast Win',
        content='...',
        author = user,
    )
    post.topics.add(topic1)

    response = client.get(reverse('mtg_blog_app:home'))
    assert response.status_code == 200
    assert b'Red Aggro' in response.content
@pytest.mark.django_db
def test_topic_list_view(client):
    """Test the topic list view"""
    Topic.objects.create(name='Favourite Art', slug='favourite-art')
    Topic.objects.create(name='MTG Lore', slug='mtg-lore')

    response = client.get(reverse('mtg_blog_app:topic_list'))
    assert response.status_code == 200
    assert 'Favourite Art' in response.content.decode()
    assert 'MTG Lore' in response.content.decode()

    topics = response.context['topics']
    assert topics[0].name == 'Favourite Art'
    assert topics[1].name == 'MTG Lore'

@pytest.mark.django_db
def test_topic_detail_view(client):
    """Test the topic detail view"""
    user = User.objects.create_user(username='testuser', password='pass')
    topic = Topic.objects.create(name='Planeswalker', slug='planeswalker')

    published_post = Post.objects.create(
        title = 'Published Post',
        content = 'Published Content',
        author = user,
        status = 'published',
    )
    published_post.topics.add(topic)

    draft_post = Post.objects.create(
        title = 'Draft Post',
        content = 'Draft Content',
        author = user,
        status = 'draft'
    )
    draft_post.topics.add(topic)

    response = client.get(reverse('mtg_blog_app:topic_detail', kwargs={'slug': topic.slug}))
    assert response.status_code == 200
    assert 'Published Post' in response.content.decode()
    assert 'Draft Post' not in response.content.decode()
    assert response.context['topic'] == topic

@pytest.fixture
def client():
    """Django test client fixture"""
    return Client()

@pytest.mark.django_db
class TestContestViews:
    """Test the contest views"""

    def test_contest_page_get(self, client):
        """Test GET request to contest page"""
        url = reverse('mtg_blog_app:contest')
        response = client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context
        assert 'Photo Contest' in response.context.decode()

    def test_contest_page_post_valid(self, client):
        """Test POST request with valid data."""
        url = reverse('mtg_blog_app:contest')
        image = SimpleUploadedFile(
            'test.jpg',
            b'fake_image_content',
            content_type='image/jpeg'
        )
        data = {
            'name' : 'Test User',
            'email' : 'test@example.com',
            'photo' : image,
        }

        response = client.post(url, data)

        assert response.status_code == 302 #redirect after successful submission
        assert PhotoSubmission.objects.count() == 1

        submission = PhotoSubmission.objects.first()
        assert submission.name == 'Test User'
        assert submission.email == 'test@example.com'

        def test_contest_page_post_invalid(self, client):
            """Test POST request with invalid data."""
            url = reverse('mtg_blog_app:contest')
            data = {
                'name' : '',
                'email' : 'test@example.com',
            }

            response = client.post(url, data)

            assert response.status_code == 200
            assert PhotoSubmission.objects.count() == 0
            assert 'form' in response.context
            assert response.context['form'].errors