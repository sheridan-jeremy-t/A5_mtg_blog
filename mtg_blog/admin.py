from django.contrib import admin
from .models import Post, Topic, Comment

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
