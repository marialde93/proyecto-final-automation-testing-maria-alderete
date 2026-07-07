"""
IMPORTANTE: reqres.in cambió su política y ahora exige una API key
(header x-api-key) en TODOS los endpoints, incluso los de lectura.
Esto es un cambio posterior a los apuntes del curso.

Para usar este test:
1. Andá a https://app.reqres.in y creá una cuenta gratis
2. Copiá tu API key
3. Definila como variable de entorno: REQRES_API_KEY=tu_key
   (o reemplazá el valor por defecto más abajo)

Si no configurás la key, este test se saltea automáticamente
en vez de fallar el pipeline completo.
"""
import os

import requests
import pytest

from utils.logger import logger

API_KEY = os.getenv("REQRES_API_KEY", "")

pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="Requiere REQRES_API_KEY configurada (ver docstring del archivo)",
)


@pytest.mark.api
@pytest.mark.parametrize(
    "email,password,expected_status",
    [
        ("eve.holt@reqres.in", "cityslicka", 200),
        ("eve.holt@reqres.in", "", 400),
    ],
    ids=["credenciales_validas", "sin_password"],
)
def test_login_reqres(reqres_login_url, email, password, expected_status):
    headers = {"x-api-key": API_KEY}
    payload = {"email": email, "password": password}

    logger.info("POST %s con email=%s", reqres_login_url, email)
    r = requests.post(reqres_login_url, json=payload, headers=headers)

    assert r.status_code == expected_status
    if expected_status == 200:
        assert "token" in r.json()
