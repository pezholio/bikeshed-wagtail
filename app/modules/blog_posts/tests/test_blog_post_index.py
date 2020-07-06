import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_blog_post_index_gets_created(blog_post_index_page):
    assert blog_post_index_page is not None

def test_blog_post_index_lists_child_posts(blog_post_index_page, blog_posts):
  rv = client.get(blog_post_index_page.url)
  assert rv.status_code == 200

  for blog_post in blog_posts:
      assert blog_post.title in str(rv.content)
