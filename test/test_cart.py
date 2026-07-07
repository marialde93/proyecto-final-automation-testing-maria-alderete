import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.logger import logger


@pytest.mark.ui
@pytest.mark.regression
def test_cart(login_in_driver):
    logger.info("Iniciando test_cart")
    inventory_page = InventoryPage(login_in_driver)

    nombre_esperado, _ = inventory_page.obtener_nombre_y_precio_primer_producto()
    inventory_page.agregar_primer_producto_al_carrito()

    contador = inventory_page.obtener_contador_carrito()
    logger.info("Contador del carrito: %s", contador)
    assert contador == "1"

    inventory_page.ir_al_carrito()

    cart_page = CartPage(login_in_driver)
    nombre_en_carrito = cart_page.obtener_nombre_primer_item()
    logger.info("Producto en carrito: %s", nombre_en_carrito)
    assert nombre_en_carrito == nombre_esperado
