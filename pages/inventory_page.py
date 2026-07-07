"""
Page Object Model - Página de Inventario/Catálogo (SauceDemo)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """Encapsula los elementos y acciones de la página de inventario."""

    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCTS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    FILTER_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def obtener_titulo(self):
        elemento = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        return elemento.text

    def obtener_productos(self):
        self.wait.until(EC.visibility_of_element_located(self.PRODUCTS))
        return self.driver.find_elements(*self.PRODUCTS)

    def menu_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENU_BUTTON)).is_displayed()

    def filtro_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.FILTER_SELECT)).is_displayed()

    def obtener_nombre_y_precio_primer_producto(self):
        nombre = self.driver.find_elements(*self.PRODUCT_NAME)[0].text
        precio = self.driver.find_elements(*self.PRODUCT_PRICE)[0].text
        return nombre, precio

    def agregar_primer_producto_al_carrito(self):
        botones = self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTONS)
        )
        botones[0].click()

    def obtener_contador_carrito(self):
        badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        return badge.text

    def ir_al_carrito(self):
        link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        link.click()
