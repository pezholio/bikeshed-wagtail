import wagtail_factories
import factory
import pytz
import pytest

from django.utils import timezone
from wagtail.core import blocks
from pytest_factoryboy import register

pytestmark = pytest.mark.django_db

class CorePageFactory(wagtail_factories.PageFactory):
    first_published_at = timezone.now()

    @factory.post_generation
    def publish(self, create, extracted, **kwargs):
      if not create:
          return
      self.save_revision().publish()

class RichTextBlockFactory(factory.Factory):
    @classmethod
    def _build(cls, model_class, value=""):
        block = model_class()
        return block.to_python(value)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._build(model_class, *args, **kwargs)

    class Meta:
        model = blocks.RichTextBlock

