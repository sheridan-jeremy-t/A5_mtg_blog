import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from mtg_blog.models import Topic, Post

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
