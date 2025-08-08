from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.views.generic import ListView, DetailView
from .models import Topic
from .forms import PhotoSubmissionForm

def home(request):
    """Create the home page when called"""
    topics = (
        Topic.objects
        .annotate(
            num_posts = Count('posts'))
        .order_by('-num_posts')[:10]
    )
    return render(request, 'mtg_blog_app/home.html', {'topics': topics})

class TopicListView(ListView):
    """List all topics alphabetically"""
    model = Topic
    template_name = 'mtg_blog_app/topic_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.all().order_by('name')

class TopicDetailView(DetailView):
    """Creating the Detail View"""
    model = Topic
    template_name = 'mtg_blog_app/topic_detail.html'
    context_object_name = 'topic'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()
        context['posts'] = topic.posts.filter(
            status = 'published'
        ).order_by('-published')
        return context

def contest_view(request):
    """View for photo contest page"""
    if request.method == 'POST':
        form = PhotoSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you for submitting to the contest! Best of luck'
            )
        return redirect(reverse('mtg_blog_app:contest'))
    else:
        form = PhotoSubmissionForm()

    context = {
        'form': form,
        'page_title' : 'Photo Contest'
    }
    return render(request, 'mtg_blog_app/contest.html', context)