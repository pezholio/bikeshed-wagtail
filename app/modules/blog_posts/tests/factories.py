import wagtail_factories
import factory
import pytest

from wagtail.core.models import Page, Site
from modules.blog_posts.models import BlogPostIndexPage, BlogPost, BlogPostTag
from modules.core.test.factories import CorePageFactory, RichTextBlockFactory
from modules.authors.tests.factories import AuthorFactory

pytestmark = pytest.mark.django_db


class BlogPostIndexFactory(CorePageFactory):
    title = "Blog"

    @factory.lazy_attribute
    def parent(self):
        return Site.objects.all()[0].root_page

    class Meta:
        model = BlogPostIndexPage


class BlogPostFactory(CorePageFactory):
    title = factory.Sequence(lambda n: "Blog Post %d" % n)
    body = wagtail_factories.StreamFieldFactory({"paragraph": RichTextBlockFactory})
    body__0__paragraph__value = "<p>This is some text</p>"

    @factory.lazy_attribute
    def parent(self):
        return BlogPostIndexFactory.create()

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    class Meta:
        model = BlogPost
