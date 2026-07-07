import pytest

from pages.inventory_page import InventoryPage
from utils.logger import logger


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_title(login_in_driver):
    logger.info("Verificando título de la página de inventario")
    inventory_page = InventoryPage(login_in_driver)
    assert inventory_page.obtener_titulo() == "Products"


@pytest.mark.ui
def test_productos_visibles(login_in_driver):
    logger.info("Verificando que haya al menos un producto visible")
    inventory_page = InventoryPage(login_in_driver)
    productos = inventory_page.obtener_productos()
    assert len(productos) > 0


@pytest.mark.ui
def test_ui_elements(login_in_driver):
    logger.info("Verificando menú y filtro de productos")
    inventory_page = InventoryPage(login_in_driver)
    assert inventory_page.menu_visible()
    assert inventory_page.filtro_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_primer_producto_nombre_y_precio(login_in_driver):
    logger.info("Obteniendo nombre y precio del primer producto")
    inventory_page = InventoryPage(login_in_driver)
    nombre, precio = inventory_page.obtener_nombre_y_precio_primer_producto()
    logger.info("Producto: %s - Precio: %s", nombre, precio)
    assert nombre != ""
    assert precio.startswith("$")
