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
        contest_url = reverse('mtg_blog_app:contest')
        response = client.get(contest_url)

        assert response.status_code == 200
        assert 'form' in response.context
        assert 'Photo Contest' in response.content.decode()

    def test_contest_page_post_valid(self, client):
        """Test POST request with valid data."""
        contest_url = reverse('mtg_blog_app:contest')

        fake_image_content = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xaa\xff\xd9'

        )

        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=fake_image_content,
            content_type='image/jpeg'
        )

        response = client.post(contest_url, {
            'name': 'Test User',
            'email': 'test@example.com',
            'photo': test_image,
        })
        # Debugging
        print(f"Response status code: {response.status_code}")
        print(f"PhotoSubmission count: {PhotoSubmission.objects.count()}")

        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            print(f"form is valid: {form.is_valid()}")
            if not form.is_valid():
                print(f"Form errors: {form.errors}")
                print(f"Form data: {form.data}")
                print(f"form files:{form.files}")

        assert response.status_code == 302 #redirect after successful submission
        assert PhotoSubmission.objects.count() == 1

        created_submission = PhotoSubmission.objects.first()
        assert created_submission.name == 'Test User'
        assert created_submission.email == 'test@example.com'

    def test_contest_page_post_invalid(self, client):
        """Test POST request with invalid data."""
        contest_url = reverse('mtg_blog_app:contest')
        invalid_data = {
            'name' : '',
            'email' : 'test@example.com',
        }

        response = client.post(contest_url, invalid_data)

        assert response.status_code == 200
        assert PhotoSubmission.objects.count() == 0
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_contest_page_success_message(self, client):
        """Test success message appears after valid submission."""
        contest_url = reverse('mtg_blog_app:contest')

        fake_image_content = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xaa\xff\xd9'
        )

        test_image = SimpleUploadedFile(
            name='success_test.jpg',
            content=fake_image_content,
            content_type='image/jpeg'
        )
        post_data = {
            'name' : 'Success User',
            'email' : 'success@example.com',
            'photo' : test_image,
        }

        response = client.post(contest_url, post_data, follow=True)

        messages = list(response.context['messages'])
        assert len(messages) == 1
        assert 'Thank you' in str(messages[0])