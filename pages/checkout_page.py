"""
Page Object Model - Flujo de Checkout (SauceDemo)

Cubre los dos pasos del checkout de SauceDemo:
1. checkout-step-one.html -> formulario con datos del comprador
2. checkout-step-two.html -> resumen y botón "Finish"
3. checkout-complete.html -> mensaje de confirmación
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """Encapsula los elementos y acciones de los 3 pasos del checkout."""

    # Paso 1: datos del comprador
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Paso 2: resumen
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    # Paso 3: confirmación
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Paso 1 ---
    def completar_datos_comprador(self, nombre, apellido, codigo_postal):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).send_keys(nombre)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(apellido)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(codigo_postal)

    def click_continue(self):
        boton = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        boton.click()

    def obtener_mensaje_error(self):
        elemento = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return elemento.text

    # --- Paso 2 ---
    def obtener_total_resumen(self):
        elemento = self.wait.until(EC.visibility_of_element_located(self.SUMMARY_TOTAL))
        return elemento.text

    def click_finish(self):
        boton = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        boton.click()

    # --- Paso 3 ---
    def obtener_mensaje_confirmacion(self):
        elemento = self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER))
        return elemento.text
