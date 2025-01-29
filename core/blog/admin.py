from django.contrib import admin
from blog.models import Image, Category, Post, Tag, Comment, CommentReply

# Register your models here.
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(CommentReply)