from django.db import models
from django.core.paginator import Paginator
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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


class BlogPostIndexPage(RoutablePageMixin, BaseIndexPage):
    subpage_types = ["BlogPost"]
    max_count = 1

    @route(r"^$")
    @route(r"^page/([0-9]+)/$")
    def all_posts(self, request, page=1):
        return render(
            request, "blog_posts/blog_post_index_page.html", self._posts_for_page(page),
        )

    @route(r"^tag/([a-z\-0-9]+)/$")
    @route(r"^tag/([a-z\-0-9]+)/page/([0-9]+)/$")
    def posts_by_tag(self, request, tag, page=1):
        objects = BlogPost.objects.filter(tags__slug=tag).distinct()

        return render(
            request,
            "blog_posts/blog_post_index_page.html",
            self._posts_for_page(page, objects),
        )

    def _posts_for_page(self, page_number, objects=None):
        if objects is None:
            objects = self.get_children().specific()
        paginator = Paginator(objects, 5)
        children = paginator.page(page_number)

        return {"page": self, "children": children, "paginator": paginator}
