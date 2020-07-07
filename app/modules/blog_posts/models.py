from wagtail.admin.edit_handlers import FieldPanel
from modules.core.models.abstract import BasePage, BaseIndexPage
from wagtail.admin.edit_handlers import StreamFieldPanel

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']
    subpage_types = []

    content_panels = [
        FieldPanel('title'),
        FieldPanel('first_published_at'),
        StreamFieldPanel('body')
    ]

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = ['BlogPost']
    max_count = 1
