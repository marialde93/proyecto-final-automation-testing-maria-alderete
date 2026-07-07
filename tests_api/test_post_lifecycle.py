import time

import requests
import pytest

from utils.logger import logger


@pytest.fixture(scope="module")
def created_post(posts_url):
    """Crea un post real vía POST y lo comparte con los tests del módulo."""
    payload = {"title": "Post para ciclo de vida", "body": "Contenido inicial", "userId": 1}
    response = requests.post(posts_url, json=payload)
    assert response.status_code == 201
    logger.info("Fixture created_post: id=%s", response.json().get("id"))
    return response.json()


@pytest.mark.api
@pytest.mark.e2e
def test_post_lifecycle_completo(post_by_id_url, created_post):
    """CRUD completo: crea (fixture) -> actualiza (PATCH) -> elimina (DELETE)
    y valida que todo el flujo corra en menos de 3s."""
    start = time.time()
    post_id = created_post["id"]
    url = post_by_id_url(post_id)

    # PATCH - actualización parcial
    logger.info("PATCH %s", url)
    patch_resp = requests.patch(url, json={"title": "Título actualizado por QA"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "Título actualizado por QA"

    # DELETE
    logger.info("DELETE %s", url)
    delete_resp = requests.delete(url)
    assert delete_resp.status_code == 200

    elapsed = time.time() - start
    logger.info("Ciclo de vida completado en %.2fs", elapsed)
    assert elapsed < 3, "El flujo completo debe ejecutarse en menos de 3s"


@pytest.mark.api
def test_put_reemplazo_completo(post_by_id_url):
    """PUT: reemplaza completamente el recurso /posts/1."""
    url = post_by_id_url(1)
    payload = {"id": 1, "title": "Automation Testing Guide", "body": "Guía completa", "userId": 1}

    logger.info("PUT %s", url)
    r = requests.put(url, json=payload)

    assert r.status_code == 200
    assert "application/json" in r.headers["Content-Type"]
    body = r.json()
    assert set(payload.keys()) <= set(body.keys())
    assert body["title"] == payload["title"]
    assert r.elapsed.total_seconds() < 1.5
