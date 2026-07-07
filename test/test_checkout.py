import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.smoke
def test_checkout_completo_exitoso(login_in_driver):
    """Flujo E2E: login -> agregar al carrito -> checkout -> confirmación."""
    logger.info("Iniciando test_checkout_completo_exitoso")
    inventory_page = InventoryPage(login_in_driver)
    inventory_page.agregar_primer_producto_al_carrito()
    inventory_page.ir_al_carrito()

    cart_page = CartPage(login_in_driver)
    cart_page.iniciar_checkout()

    checkout_page = CheckoutPage(login_in_driver)
    checkout_page.completar_datos_comprador("Maria", "Alderete", "1900")
    checkout_page.click_continue()

    total = checkout_page.obtener_total_resumen()
    logger.info("Total del resumen: %s", total)
    assert "Total" in total

    checkout_page.click_finish()

    mensaje = checkout_page.obtener_mensaje_confirmacion()
    logger.info("Mensaje de confirmación: %s", mensaje)
    assert mensaje == "Thank you for your order!"


@pytest.mark.ui
@pytest.mark.e2e
def test_checkout_sin_datos_muestra_error(login_in_driver):
    """Escenario negativo: continuar sin completar los datos del comprador."""
    logger.info("Iniciando test_checkout_sin_datos_muestra_error")
    inventory_page = InventoryPage(login_in_driver)
    inventory_page.agregar_primer_producto_al_carrito()
    inventory_page.ir_al_carrito()

    cart_page = CartPage(login_in_driver)
    cart_page.iniciar_checkout()

    checkout_page = CheckoutPage(login_in_driver)
    checkout_page.click_continue()  # sin completar nada

    error = checkout_page.obtener_mensaje_error()
    logger.info("Error recibido: %s", error)
    assert "First Name is required" in error
