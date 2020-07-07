import pytest
from django.test import Client
from modules.blog_posts.models import BlogPost, BlogPostIndexPage

pytestmark = pytest.mark.django_db

client = Client()

def test_blog_post_gets_created(blog_post):
    """Test that we have a blog post created by the fixture
    """
    assert blog_post is not None

def test_blog_post_has_the_correct_title(blog_post):
    """Test that the blog post has the expected title
    """
    blog_post.title = "Here is a blog post"
    blog_post.save()
    assert blog_post.title == "Here is a blog post"

def test_blog_post_title_is_visible(blog_post):
    """Test that the blog post title and content is visible in the template
    """
    rv = client.get(blog_post.url)

    assert blog_post.title in str(rv.content)

def test_blog_post_tags_are_visible(blog_post):
    """Test that a blog post's tags are visible on the blog post template
    """
    blog_post.tags.add("foo", "bar", "baz")
    blog_post.save_revision().publish()
    blog_post.save()

    rv = client.get(blog_post.url)

    assert "foo" in str(rv.content)
    assert "bar" in str(rv.content)
    assert "baz" in str(rv.content)


def test_blog_post_cannot_have_subpages():
    """Test that blog posts cannot have subpages
    """
    assert BlogPost.allowed_subpage_models() == []

def test_blog_posts_parent_pages():
    """Test that blog posts cannot have subpages
    """
    assert BlogPost.allowed_parent_page_models() == [
        BlogPostIndexPage
    ]

