import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from mtg_blog.models import Topic, Post
from mtg_blog.context_processors import base_context

@pytest.fixture
def user(db):
    """Setup of User"""
    return User.objects.create_user(
        username = 'testuser',
        password= 'password123'
    )
@pytest.fixture
def topics_with_posts(db, user):
    """Test for Post count"""
    topic1 = Topic.objects.create(name='Python', slug = 'python')
    topic2 = Topic.objects.create(name='Django', slug = 'django')
    topic3 = Topic.objects.create(name='Web Development', slug = 'web-development') #Create to make sure it doesn't show even if the topic is created it doesnt show is there are no posts with the topic

    for i in range(5):
        post = Post.objects.create(
            title = f'Python Post {i}',
            content = f'Test content for Python post {i}',
            author = user,
            status = 'published',
        )
        post.topics.add(topic1)

    for i in range(3):
        post = Post.objects.create(
            title = f'Django Post {i}',
            content = f'Test content for Django post {i}',
            author = user,
            status = 'published',
        )
        post.topics.add(topic2)

    return topic1, topic2, topic3

def test_base_context_returns_top_topics(topics_with_posts):
    """Test that base context returns top topics"""
    topic1, topic2, topic3 = topics_with_posts
    factory = RequestFactory()
    request = factory.get('/')
    context = base_context(request)

    assert 'top_topics' in context
    assert len(context['top_topics']) == 2
    assert context['top_topics'][0] == topic1
    assert context['top_topics'][1] == topic2
