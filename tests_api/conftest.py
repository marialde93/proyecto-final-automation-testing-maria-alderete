import pytest

REQRES_BASE = "https://reqres.in/api"
JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="module")
def reqres_users_url():
    return f"{REQRES_BASE}/users"


@pytest.fixture(scope="module")
def reqres_login_url():
    return f"{REQRES_BASE}/login"


@pytest.fixture(scope="module")
def posts_url():
    return f"{JSONPLACEHOLDER_BASE}/posts"


@pytest.fixture(scope="module")
def post_by_id_url():
    def _get_url(post_id):
        return f"{JSONPLACEHOLDER_BASE}/posts/{post_id}"
    return _get_url
