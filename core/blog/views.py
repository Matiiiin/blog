from django.shortcuts import render
from django.views.generic import ListView
from .models import Category , Post
from django.db.models import Count

class CategoryResultTemplateView(ListView):
    template_name = 'blog/category_result_page/main.html'
    paginate_by = 5
    context_object_name = 'category_posts'
    page_kwarg = "page"
    ordering = '-created_at'
    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        category_posts = Category.objects.get(name=category_name).posts.select_related('author').all()
        return category_posts
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs.get('category_name')
        context['popular_posts'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
        context['categories'] = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
        return context
