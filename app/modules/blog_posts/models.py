from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPost(BasePage):
  parent_page_types = ['BlogPostIndexPage']

class BlogPostIndexPage(BaseIndexPage):
  pass
