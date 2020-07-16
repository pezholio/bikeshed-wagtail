from django.db import models
from django.core.paginator import Paginator
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from modules.core.models.abstract import BasePage, BaseIndexPage
from wagtail.admin.edit_handlers import StreamFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalManyToManyField


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog_posts.BlogPost",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class BlogPost(BasePage):
    parent_page_types = ["BlogPostIndexPage"]
    subpage_types = []

    authors = ParentalManyToManyField(
        "authors.Author", blank=False, related_name="pages_%(class)s"
    )

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("first_published_at"),
        FieldPanel("authors", widget=ModelSelect2Multiple(url="author-autocomplete")),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]

    def author_list(self):
        return (", ").join(map(lambda author: author.name, self.authors.all()))


class BlogPostIndexPage(BaseIndexPage):
    subpage_types = ["BlogPost"]
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        request_tags = request.GET.get("tag", None)
        page = int(request.GET.get("page", 1))

        if request_tags:
            tags = request_tags.split(",")
            objects = BlogPost.objects.filter(tags__slug__in=tags).distinct()
        else:
            objects = context["page"].get_children()

        paginator = Paginator(objects, 5)
        children = paginator.page(page)

        context.update({"children": children, "paginator": paginator})

        return context
