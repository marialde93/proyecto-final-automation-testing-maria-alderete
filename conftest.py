import datetime
import os
import pathlib

import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from utils.logger import logger

# ── Fixtures originales de la pre-entrega (se mantienen igual) ──────────────


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    # En CI (GitHub Actions) no hay pantalla disponible: forzamos headless.
    # Localmente, si querés ver el navegador correr, dejalo como está.
    if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("HEADLESS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_in_driver(driver):
    """Loguea con el usuario estándar y devuelve el driver ya autenticado."""
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    return driver


# ── Capturas de pantalla automáticas en fallos de UI ─────────────────────────

target = pathlib.Path("reports/screens")
target.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Toma un screenshot cuando un test UI falla en la fase 'call'
    y lo adjunta al reporte HTML de pytest-html.

    IMPORTANTE: no usamos hasattr(report, "extra") para decidir si adjuntar,
    porque pytest-html crea ese atributo en su propio hookwrapper y, al ser
    nuestro hook tryfirst=True, puede ejecutarse antes. Por eso construimos
    la lista con getattr(..., []) y la reasignamos siempre al final.
    """
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver") or item.funcargs.get(
            "login_in_driver"
        )
        if driver_fixture:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = target / f"{item.name}_{timestamp}.png"
            try:
                driver_fixture.save_screenshot(str(file_name))
                logger.error(
                    "Screenshot guardado en %s tras fallo de %s", file_name, item.name
                )
                extra.append(
                    {"name": "screenshot", "format": "image", "content": str(file_name)}
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("No se pudo guardar el screenshot: %s", exc)

    report.extra = extra


# ── Columna URL extra en la tabla del reporte HTML ───────────────────────────


def pytest_html_report_title(report):
    report.title = "Proyecto Final - Framework de Automatización QA (Alderete)"


def pytest_html_results_table_header(cells):
    cells.insert(2, "URL")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, getattr(report, "page_url", "-"))
