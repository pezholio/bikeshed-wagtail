import pytest
import json
from django.test import Client
from django.contrib.auth.models import User
from modules.authors.tests.factories import AuthorFactory

pytestmark = pytest.mark.django_db

client = Client()


class TestAuthor:
    def test_authors_can_be_filtered(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        client.login(username="testuser", password="12345")

        author1 = AuthorFactory.create(name="John Smith")
        AuthorFactory.create(name="Jane Smith")

        rv = client.get("/author-autocomplete/", {"q": "Jo"})
        data = json.loads(rv.content)

        assert len(data["results"]) == 1
        assert data["results"][0]["text"] == author1.name + " (" + author1.email + ")"
