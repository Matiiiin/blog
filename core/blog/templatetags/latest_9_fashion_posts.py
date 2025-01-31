from django import template
from blog.models import Post
import logging

logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def latest_9_fashion_posts():
    try:
        return Post.objects.filter(category__name='Fashion').select_related('author').order_by('-created_at')[:9]
    except Exception as e:
        logger.error(f"Exception in latest_9_fashion_posts, details:{e}")
        return []
