import json
import pathlib

import pytest

from pages.login_page import LoginPage
from utils.logger import logger

DATA_PATH = pathlib.Path(__file__).parent.parent / "utils" / "data" / "login_data.json"
with open(DATA_PATH, encoding="utf-8") as f:
    LOGIN_DATA = json.load(f)


@pytest.mark.ui
@pytest.mark.smoke
def test_login_ok(driver):
    """Login con credenciales válidas redirige a inventory.html."""
    logger.info("Iniciando test_login_ok")
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    logger.info("Verificando redirección a inventory.html")
    assert "inventory.html" in driver.current_url
    logger.info("test_login_ok completado exitosamente")


@pytest.mark.ui
def test_login_invalid_password(driver):
    """Login con password incorrecta muestra el mensaje de error."""
    logger.info("Iniciando test_login_invalid_password")
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.ingresar_usuario("standard_user")
    login_page.ingresar_password("password_incorrecta")
    login_page.click_login()

    error = login_page.obtener_mensaje_error()
    logger.info("Mensaje de error recibido: %s", error)
    assert "do not match" in error.lower() or "epsilon" in error.lower() or error != ""


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "caso",
    LOGIN_DATA["casos_validos"],
    ids=[c["descripcion"] for c in LOGIN_DATA["casos_validos"]],
)
def test_login_usuarios_validos(driver, caso):
    """Parametrizado: valida login con distintos usuarios válidos (data externa)."""
    logger.info("Probando login con %s (%s)", caso["username"], caso["descripcion"])
    login_page = LoginPage(driver)
    login_page.login(caso["username"], caso["password"])
    assert "inventory.html" in driver.current_url


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "caso",
    LOGIN_DATA["casos_invalidos"],
    ids=[c["descripcion"] for c in LOGIN_DATA["casos_invalidos"]],
)
def test_login_usuarios_invalidos(driver, caso):
    """Parametrizado: valida que credenciales inválidas nunca permitan el acceso."""
    logger.info("Probando login inválido: %s", caso["descripcion"])
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.ingresar_usuario(caso["username"])
    login_page.ingresar_password(caso["password"])
    login_page.click_login()
    assert "inventory.html" not in driver.current_url
