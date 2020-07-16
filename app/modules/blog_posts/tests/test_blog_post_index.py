import pytest
from django.test import Client

from modules.blog_posts.models import BlogPostIndexPage, BlogPost
from modules.blog_posts.tests.factories import BlogPostIndexFactory, BlogPostFactory

pytestmark = pytest.mark.django_db

client = Client()


class TestBlogPostIndex:
    def test_blog_post_index_gets_created(self):
        blog_post_index_page = BlogPostIndexFactory.create()
        assert blog_post_index_page is not None

    def test_blog_post_index_lists_child_posts(self):
        blog_post_index_page = BlogPostIndexFactory.create()
        blog_posts = BlogPostFactory.create_batch(10, parent=blog_post_index_page)

        page1 = client.get(blog_post_index_page.url)
        assert page1.status_code == 200

        page2 = client.get(blog_post_index_page.url + "page/2/")
        assert page2.status_code == 200

        for blog_post in blog_posts[:5]:
            assert blog_post.title in str(page1.content)

        for blog_post in blog_posts[5:10]:
            assert blog_post.title in str(page2.content)

    def test_blog_post_index_filters_by_tag(self):
        blog_post_index_page = BlogPostIndexFactory.create()
        tagged_post = BlogPostFactory.create(tags=["foo"], parent=blog_post_index_page)
        untagged_post = BlogPostFactory.create(
            tags=["bar"], parent=blog_post_index_page
        )

        rv = client.get(blog_post_index_page.url + "tag/foo/")

        assert tagged_post.title in str(rv.content)
        assert untagged_post.title not in str(rv.content)

    def test_blog_post_index_page_subpages(self):
        """Test that blog posts cannot have subpages
        """
        assert BlogPostIndexPage.allowed_subpage_models() == [BlogPost]

    def test_blog_post_index_page_has_pagination(self):
        blog_post_index_page = BlogPostIndexFactory.create()
        BlogPostFactory.create_batch(60, parent=blog_post_index_page)

        rv = client.get(blog_post_index_page.url)
        assert rv.status_code == 200

        assert '<a class="current" href="/blog/page/1">1</a>' in str(rv.content)
        assert '<a href="/blog/page/2">2</a>' in str(rv.content)
        assert '<a href="/blog/page/3">3</a>' in str(rv.content)
        assert '<a href="/blog/page/4">4</a>' in str(rv.content)
        assert '<a href="/blog/page/5">5</a>' in str(rv.content)
        assert "<li>...</li>" in str(rv.content)
        assert '<a href="/blog/page/2">Next</a>' in str(rv.content)
