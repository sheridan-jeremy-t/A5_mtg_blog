"""Models for MTG Site"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

class Topic(models.Model):
    """Creating the Topic models"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        """Get the absolute url for the topic"""
        return reverse('mtg_blog_app:topic_detail', kwargs= {'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Post(models.Model):
    """Creating the models for Post"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mtg_posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published = models.DateTimeField(null=True,blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='posts')

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        #Set timestamp when published
        if self.status == 'published' and not self.published:
            self.published = timezone.now()
        elif self.status =='draft':
            self.published = None

        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Creating the Comment Model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField(max_length=500)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'

    class Meta:
        ordering = ['-created']

class PhotoSubmission(models.Model):
    """Model for photo contest submission"""

    name = models.CharField(max_length=100, help_text='Your full name')
    email = models.EmailField(help_text='Your email address')
    photo = models.ImageField(
        upload_to='contest_photos/',
        help_text='Upload your contest photo'
    )
    submission_date = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time of submission'
    )

    class Meta:
        """Meta options for Photo Submissions"""
        ordering = ['-submission_date']
        verbose_name='Photo Submission'
        verbose_name_plural='Photo Submissions'

    def __str__(self):
        """String representation of Photo Submission"""
        return f"Photo Submission by {self.name} on {self.submission_date.strftime('%Y-%m-%d')}"
