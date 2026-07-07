"""
Page Object Model - Página de Login (SauceDemo)
Reemplaza/extiende a utils/LoginPage.py manteniendo compatibilidad.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"


class LoginPage:
    """Encapsula los elementos y acciones de la página de login."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir(self):
        """Navega a la página de login."""
        self.driver.get(URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        return self

    def ingresar_usuario(self, username):
        campo = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        campo.clear()
        campo.send_keys(username)

    def ingresar_password(self, password):
        campo = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        campo.clear()
        campo.send_keys(password)

    def click_login(self):
        boton = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        boton.click()

    def login(self, username, password):
        """Flujo completo de login. Mantiene compatibilidad con la fixture
        login_in_driver, que espera poder loguear con un solo llamado."""
        self.abrir()
        self.ingresar_usuario(username)
        self.ingresar_password(password)
        self.click_login()

    def obtener_mensaje_error(self):
        elemento = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return elemento.text
