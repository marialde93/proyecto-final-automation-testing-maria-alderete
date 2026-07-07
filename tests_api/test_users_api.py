import requests
import pytest

from utils.logger import logger


@pytest.mark.api
@pytest.mark.smoke
def test_get_posts_status_y_estructura(posts_url):
    """GET a /posts: valida status, cabeceras, estructura y performance (5 niveles)."""
    logger.info("GET %s", posts_url)
    r = requests.get(posts_url)

    # Nivel 1: status
    assert r.status_code == 200
    # Nivel 2: cabeceras
    assert "application/json" in r.headers["Content-Type"]
    # Nivel 3: estructura
    data = r.json()
    assert len(data) > 0
    assert {"id", "title", "body", "userId"} <= set(data[0].keys())
    # Nivel 4: contenido
    assert all(isinstance(post["id"], int) for post in data[:5])
    # Nivel 5: performance
    assert r.elapsed.total_seconds() < 2
    logger.info("test_get_posts_status_y_estructura OK - %s posts recibidos", len(data))


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_get_post_por_id(post_by_id_url, post_id):
    """GET parametrizado: valida distintos posts por id."""
    url = post_by_id_url(post_id)
    logger.info("GET %s", url)
    r = requests.get(url)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == post_id
    assert "title" in data and data["title"] != ""


@pytest.mark.api
def test_get_post_inexistente(post_by_id_url):
    """Escenario negativo: pedir un post que no existe devuelve 404."""
    url = post_by_id_url(99999)
    logger.info("GET %s (post inexistente)", url)
    r = requests.get(url)
    assert r.status_code == 404
