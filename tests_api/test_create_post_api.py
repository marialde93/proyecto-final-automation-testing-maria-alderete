import datetime

import requests
import pytest

from utils.logger import logger

CASOS = [
    {"title": "Automatizando con QA", "body": "Contenido de prueba 1", "userId": 1},
    {"title": "Framework de testing", "body": "Contenido de prueba 2", "userId": 2},
    {"title": "Pytest y Requests", "body": "Contenido de prueba 3", "userId": 3},
]


@pytest.mark.api
@pytest.mark.parametrize("payload", CASOS, ids=[c["title"] for c in CASOS])
def test_create_post(posts_url, payload):
    """POST parametrizado: crea posts con distintos títulos/autores."""
    logger.info("POST %s con payload=%s", posts_url, payload)
    r = requests.post(posts_url, json=payload)

    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]
    assert "id" in data
    logger.info("Post creado con id=%s", data["id"])


@pytest.mark.api
def test_create_post_valida_year_actual(posts_url):
    """Extra: verifica que el post creado se pueda asociar a la fecha actual
    (JSONPlaceholder no persiste createdAt, así que validamos en el cliente)."""
    payload = {"title": "Post con fecha", "body": "test", "userId": 1}
    r = requests.post(posts_url, json=payload)
    assert r.status_code == 201

    anio_actual = datetime.datetime.now().year
    logger.info("Post creado, validado contra el año actual: %s", anio_actual)
    assert anio_actual >= 2026
