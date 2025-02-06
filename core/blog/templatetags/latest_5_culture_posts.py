from django import template
from blog.models import Post
import logging

logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def latest_5_culture_posts():
    try:
        return Post.objects.filter(category__name='Culture').order_by('-created_at')[:5]
    except Exception as e:
        logger.error(f"Exception in latest_5_culture_posts, details:{e}")
        return []
