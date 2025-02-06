from django import template
from blog.models import Post
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def latest_4_travel_posts():
    try:
        return Post.objects.filter(category__name="Travel").order_by(
            "-created_at"
        )[:4]
    except Exception as e:
        logger.error(
            f"Exception in latest_4_travel_posts, details:{e}"
        )
        return []
