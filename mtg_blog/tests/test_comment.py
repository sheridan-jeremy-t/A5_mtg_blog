from freezegun import freeze_time
from django.test import TestCase
from django.contrib.auth.models import User
from mtg_blog.models import Comment, Post

class TestCommentModel(TestCase):
    """Test Comment Model"""
    def setUp(self):
        self.user = User.objects.create_user(
            username= 'mtgplayer',
            email= 'player@example.com',
            password = 'manaburn123',
        )
        self.post = Post.objects.create(
            title = 'Modern Horizons 3 Card Review',
            author = self.user,
            slug = 'modern-horizons-3-review',
        )
    def test_comment_creation(self):
        """Test comment model creation"""
        comment = Comment.objects.create(
            post = self.post,
            name = 'Commander Player',
            email = 'commander@example.com',
            text = 'Great review! This card will be amazing in my Eldrazi deck!',
            approved = True
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.name, 'Commander Player')
        self.assertEqual(comment.approved, True)
        self.assertIsNotNone(comment.created)

    def test_comment_str_method(self):
        """Test Comment string representation"""
        comment = Comment.objects.create(
            post = self.post,
            name = 'Standard Player',
            email = 'standard@example.com',
            text = 'This will shake up the meta!',
        )
        expected_str = f'Comment by Standard Player on {self.post.title}'
        self.assertEqual(str(comment), expected_str)

    def test_comment_default_ordering(self):
        """Test comment default ordering by newest first"""
        with freeze_time("2025-07-14 09:00:00"):
            comment1 = Comment.objects.create(
                post = self.post,
                name = 'First Commenter',
                email = 'first@example.com',
                text = 'First comment about sideboard choices',
            )
        with freeze_time("2025-07-14 10:00:00"):
            comment2 = Comment.objects.create(
                post=self.post,
                name='Second Commenter',
                email='second@example.com',
                text='Second comment about sideboard choices',
            )
        comments = Comment.objects.all()
        self.assertEqual(comments[0], comment2) #most recent first
        self.assertEqual(comments[1], comment1)
