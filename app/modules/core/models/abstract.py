from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core import blocks
from wagtail.search import index


class BasePage(Page):
    class Meta:
        abstract = True

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    search_fields = Page.search_fields + [
        index.SearchField("search_description", boost=10),
        index.SearchField("title", boost=5),
        index.SearchField("body"),
    ]


class BaseIndexPage(BasePage):
    class Meta:
        abstract = True
