from django.urls import path , include
from . import views
app_name = 'blog'
urlpatterns = [
    path('api/v1/', include('blog.api.v1.urls')),
    path('category-result/<str:category_name>' , views.CategoryResultTemplateView.as_view() , name='category-result'),
    path('post/<slug:slug>' , views.PostDetailView.as_view() , name='post-detail'),
    path('comment/<int:comment_id>/comment-reply/create/' , views.CommentReplyView.as_view() , name='comment-reply-create'),
    path('post/<slug:post_slug>/comment/create' , views.CommentView.as_view() , name='comment-create'),
    path('' , views.PostListView.as_view() , name='post-list'),
]