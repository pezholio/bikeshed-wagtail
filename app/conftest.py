import pytest

from modules.home.tests.fixtures import *
from modules.blog_posts.tests.fixtures import *
from modules.authors.tests.fixtures import *

pytestmark = pytest.mark.django_db
