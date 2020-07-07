import pytest
from django.test import Client
from modules.blog_posts.models import BlogPost, BlogPostIndexPage

pytestmark = pytest.mark.django_db

client = Client()

def test_blog_post_index_gets_created(blog_post_index_page):
    assert blog_post_index_page is not None

def test_blog_post_index_lists_child_posts(blog_post_index_page, blog_posts):
  rv = client.get(blog_post_index_page.url)
  assert rv.status_code == 200

  for blog_post in blog_posts:
      assert blog_post.title in str(rv.content)

def test_blog_post_index_filters_by_tag(blog_post_index_page, blog_posts):
    blog_posts[0].tags.add('foo')
    blog_posts[0].save()

    blog_posts[1].tags.add('bar')
    blog_posts[1].save()

    rv = client.get(blog_post_index_page.url + "?tag=foo")

    assert blog_posts[0].title in str(rv.content)
    assert blog_posts[1].title not in str(rv.content)

def test_blog_post_index_page_subpages():
    """Test that blog posts cannot have subpages
    """
    assert BlogPostIndexPage.allowed_subpage_models() == [
        BlogPost
    ]
