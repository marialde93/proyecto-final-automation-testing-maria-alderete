"""
Page Object Model - Página de Carrito (SauceDemo)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Encapsula los elementos y acciones de la página de carrito."""

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def obtener_items(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_ITEM))
        return self.driver.find_elements(*self.CART_ITEM)

    def obtener_nombre_primer_item(self):
        items = self.obtener_items()
        return items[0].find_element(*self.CART_ITEM_NAME).text

    def iniciar_checkout(self):
        """Hace click en 'Checkout' para pasar al formulario de datos del comprador."""
        boton = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        boton.click()
