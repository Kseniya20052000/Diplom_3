import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.register_page import RegisterPage


class LoginPage(BasePage):

    URL = "https://stellarburgers.education-services.ru/login"

    EMAIL_INPUT = (By.XPATH, "//fieldset[.//label[text()='Email']]//input")
    PASSWORD_INPUT = (By.XPATH, "//fieldset[.//label[text()='Пароль']]//input")

    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/register']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")

    @allure.step("Переходим на страницу регистрации")
    def go_to_register(self) -> RegisterPage:
        self.click(self.REGISTER_LINK)
        register_page = RegisterPage(self.driver)
        register_page.wait_visible(RegisterPage.NAME_INPUT)
        return register_page

    @allure.step("Входим под пользователем: {email}")
    def login(self, email: str, password: str):
        self.wait_visible(self.EMAIL_INPUT).send_keys(email)
        self.wait_visible(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)
