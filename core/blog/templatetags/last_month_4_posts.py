from django import template
from blog.models import Post
import logging
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def last_month_4_posts():
    try:
        last_month = datetime.now().today() - timedelta(days=30)
        date_from = timezone.datetime(
            last_month.year,
            last_month.month,
            last_month.day,
            0,
            0,
            0,
            tzinfo=timezone.get_current_timezone(),
        )

        date_to = date_from + timedelta(days=30)

        posts = Post.objects.filter(
            created_at__range=(date_from, date_to)
        ).order_by("-created_at")[:4]
        if posts:
            return posts
        else:
            return Post.objects.order_by("?")[:4]
    except Exception as e:
        logger.error(f"Exception in last_month_4_posts, details:{e}")
        return []
