from django.contrib import admin
from .models import Post, Topic, Comment, PhotoSubmission

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Topic Class"""
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

class CommentInline(admin.TabularInline):
    """Comment line class"""
    model = Comment
    fields = ('name','email', 'text', 'approved')
    readonly_fields = ('name', 'email', 'text')
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post Class"""
    list_display = ('title', 'created', 'updated', 'status', 'author')
    list_filter = ('status', 'topics')
    search_fields = ('title', 'author__username', 'author__first_name', 'author__lastname')
    prepopulated_fields = {'slug':('title',)}
    ordering = ('created',)
    filter_horizontal = ('topics',)
    inlines = [CommentInline]
    #set the order of the fields on the page
    fields = ('title', 'slug',  'status', 'author','content','topics')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment sort class"""
    list_display = ('name', 'post', 'created', 'approved')
    list_filter = ('approved', 'created')
    search_fields = ('name', 'email', 'text')

@admin.register(PhotoSubmission)
class PhotoSubmissionAdmin(admin.ModelAdmin):
    """Admin config for PhotoSubmission"""
    list_display = ['name', 'email', 'submission_date', 'photo_thumbnail']
    list_filter = ['submission_date']
    search_fields = ['name', 'email',]
    readonly_fields = ['submission_date', 'photo_thumbnail']
    ordering = ['-submission_date',]

    def photo_thumbnail(self, obj):
        """Display thumbnail in list view"""
        if obj.photo:
            return f'<img source="{obj.photo.url}" width="50" height="50" style="object-fit: cover;"/>'
        return "No Photo"
    photo_thumbnail.short_description = 'Photo'
    photo_thumbnail.allow_tags = True

    def photo_preview(self, obj):
        """Display preview in detail view"""
        if obj.photo:
            return f'<img source="{obj.photo.url}" width="300" height="300" style="max-width: 300px;">'
        return "No Photo Uploaded"

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True
