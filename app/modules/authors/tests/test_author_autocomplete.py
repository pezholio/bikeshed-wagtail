import pytest
import json
from django.test import Client
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

client = Client()

def test_authors_can_be_filtered(authors):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    client.login(username='testuser', password='12345')

    authors[0].name = "John Smith"
    authors[0].save()

    authors[1].name = "Jane Smith"
    authors[1].save()

    rv = client.get("/author-autocomplete/", {"q": "Jo"})
    data = json.loads(rv.content)

    assert len(data['results']) == 1
    assert data['results'][0]['text'] == "John Smith (user0@example.com)"



