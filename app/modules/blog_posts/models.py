from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from modules.core.models.abstract import BasePage, BaseIndexPage
from wagtail.admin.edit_handlers import StreamFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog_posts.BlogPost',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']
    subpage_types = []

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('first_published_at'),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
    ]

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = ['BlogPost']
    max_count = 1
