"""
Se mantiene por compatibilidad con la pre-entrega original.
La lógica real vive ahora en pages/login_page.py (POM formal).
"""
from pages.login_page import LoginPage


def login(driver, username="standard_user", password="secret_sauce"):
    """Función auxiliar original: loguea con credenciales válidas por defecto."""
    page = LoginPage(driver)
    page.login(username, password)
