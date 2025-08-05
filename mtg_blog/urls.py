from django.urls import path
from . import views

app_name = 'mtg_blog_app'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('topics/', views.TopicListView.as_view(), name='topic_list'),
    path('topic/<slug:slug>', views.TopicDetailView.as_view(), name = 'topic_detail'),
]
