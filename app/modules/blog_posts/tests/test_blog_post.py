import pytest

from django.test import Client
from modules.blog_posts.models import BlogPost, BlogPostIndexPage
from wagtail.core.models import Page, Site
from modules.blog_posts.tests.factories import BlogPostFactory, BlogPostIndexFactory
from modules.authors.tests.factories import AuthorFactory

client = Client()

pytestmark = pytest.mark.django_db


class TestBlogPost:
    def test_blog_post_gets_created(self):
        """Test that we have a blog post created by the fixture
        """
        blog_post = BlogPostFactory.create()
        assert blog_post is not None

    def test_blog_post_has_the_correct_title(self):
        """Test that the blog post has the expected title
        """
        blog_post = BlogPostFactory.create(title="Here is a blog post")
        assert blog_post.title == "Here is a blog post"

    def test_blog_post_title_is_visible(self):
        """Test that the blog post title and content is visible in the template
        """
        blog_post = BlogPostFactory.create()
        rv = client.get(blog_post.url)

        assert blog_post.title in str(rv.content)

    def test_blog_post_tags_are_visible(self):
        """Test that a blog post's tags are visible on the blog post template
        """
        blog_post = BlogPostFactory.create(tags=("foo", "bar", "baz"))

        rv = client.get(blog_post.url)

        assert "foo" in str(rv.content)
        assert "bar" in str(rv.content)
        assert "baz" in str(rv.content)

    def test_author_is_visible(self):
        blog_post = BlogPostFactory.create(authors=[AuthorFactory(name="Jane Smith")])

        rv = client.get(blog_post.url)

        assert ("Jane Smith") in str(rv.content)

    def test_blog_post_cannot_have_subpages(self):
        """Test that blog posts cannot have subpages
        """
        assert BlogPost.allowed_subpage_models() == []

    def test_blog_posts_parent_pages(self):
        """Test that blog posts cannot have subpages
        """
        assert BlogPost.allowed_parent_page_models() == [BlogPostIndexPage]
