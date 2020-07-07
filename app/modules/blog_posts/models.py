from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']
    subpage_types = []

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = ['BlogPost']
    max_count = 1
