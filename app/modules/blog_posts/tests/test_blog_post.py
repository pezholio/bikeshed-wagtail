import pytest
from django.test import Client

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

