from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.image.url

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('account.Profile', on_delete=models.CASCADE , related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.CASCADE , related_name='posts')
    images = models.ManyToManyField('Image', related_name='posts')
    tags = models.ManyToManyField('Tag', related_name='posts')
    title = models.CharField(max_length=100 , unique=True , blank=False , null=False)
    slug = models.SlugField(max_length=100 , unique=True , blank=True , null=True)
    hero_image = models.ImageField(upload_to='post_images/')
    short_content = models.TextField()
    main_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE , related_name='comments')
    author = models.ForeignKey('account.Profile', on_delete=models.CASCADE , related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class CommentReply(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE , related_name='replies')
    author = models.ForeignKey('account.Profile', on_delete=models.CASCADE , related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
