import factory
import pytest

from modules.authors.models import Author

pytestmark = pytest.mark.django_db

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
    email = factory.Faker('email')
