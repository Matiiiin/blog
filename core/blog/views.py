from django.shortcuts import render
from django.views.generic import ListView , DetailView , CreateView
from django.views import View
from .models import Category , Post , CommentReply,Comment
from django.db.models import Count
from django.shortcuts import redirect
from .forms import CommentForm
from django.db.models import Q

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class CategoryResultTemplateView(ListView):
    template_name = 'blog/category_result_page/main.html'
    paginate_by = 5
    context_object_name = 'category_posts'
    page_kwarg = "page"
    ordering = '-created_at'

    @method_decorator(cache_page(60 * 10, key_prefix='category-result'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

class PostDetailView(DetailView):
    template_name = 'blog/post_detail_page/main.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        post = Post.objects.filter(slug=self.kwargs.get('slug')).select_related('author' , 'category').prefetch_related('images' ,'comments').all()
        return post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['popular_posts'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
        context['categories'] = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
        context['more_posts'] = Post.objects.all().order_by('?')[:4]
        return context
class CommentReplyView(View):
    def post(self , request , comment_id):
        comment = Comment.objects.get(id=comment_id)
        CommentReply.objects.create(
            comment=comment,
            author=request.user.profile,
            content=request.POST.get('content')
        )
        return redirect('blog:post-detail' , slug=comment.post.slug)
class CommentView(View):
    def post(self , request , post_slug):
        post = Post.objects.get(slug=post_slug)
        Comment.objects.create(
            post=post,
            author=request.user.profile,
            content=request.POST.get('content')
        )
        return redirect('blog:post-detail' , slug=post_slug)
class PostListView(ListView):
    template_name = 'blog/post_list_page/main.html'
    paginate_by = 5
    model = Post
    context_object_name = 'posts'
    ordering = '-created_at'

    @method_decorator(cache_page(60 * 10, key_prefix='post-list'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
        context['categories'] = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
        return context
class SearchTemplateView(ListView):
    template_name = 'blog/search_result_page/main.html'
    paginate_by = 5
    context_object_name = 'posts'
    page_kwarg = "page"
    ordering = '-created_at'
    def get_queryset(self):
        search = self.request.GET.get('search')
        posts = Post.objects.filter(
            Q(title__icontains=search) |
            Q(main_content__icontains=search) |
            Q(short_content__icontains=search) |
            Q(author__first_name__icontains=search) |
            Q(author__last_name__icontains=search)
        ).all()
        return posts
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        context['popular_posts'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
        context['categories'] = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
        return context