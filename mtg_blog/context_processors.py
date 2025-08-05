from django.db.models import Count
from .models import Topic

def base_context(request):
    """Calculate Number of posts per Topic"""
    top_topics = (Topic.objects
    .annotate(post_count=Count('posts')
    ).filter(post_count__gt = 0
    ).order_by('-post_count')[:5]
)

    return {'top_topics' : top_topics,}
