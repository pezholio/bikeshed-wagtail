from typing import List
import pytest

from modules.authors.models import Author

pytestmark = pytest.mark.django_db

def _create_author(name: str, email: str) -> Author:
    p = Author(
      name=name,
      email=email
    )
    p.save()
    return p

@pytest.fixture(scope="function")
def author() -> Author:
    p = _create_author('Example User', 'user@example.com')
    return p

@pytest.fixture(scope="function")
def authors() -> List[Author]:
    rv = []
    for _ in range(0, 10):
        p = _create_author(f'Example User {_}', f'user{_}@example.com')
        rv.append(p)
    return rv
