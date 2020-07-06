import pytest

from wagtail.core.models import Page
from modules.home.models import HomePage

def _create_home_page(title: str, parent: Page) -> HomePage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title

    Returns:
        HomePage: Description
    """
    p = HomePage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p

@pytest.fixture(scope="function")
def home_page(site_root) -> HomePage:
    p = _create_home_page('Home', site_root)
    return p
