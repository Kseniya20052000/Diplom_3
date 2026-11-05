import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):

    URL = "https://stellarburgers.education-services.ru/register"

    NAME_INPUT = (By.XPATH, "//fieldset[.//label[text()='Имя']]//input")
    EMAIL_INPUT = (By.XPATH, "//fieldset[.//label[text()='Email']]//input")
    PASSWORD_INPUT = (By.XPATH, "//fieldset[.//label[text()='Пароль']]//input")

    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")

    @allure.step("Регистрируем пользователя: {email}")
    def register(self, name: str, email: str, password: str):
        self.wait_visible(self.NAME_INPUT).send_keys(name)
        self.wait_visible(self.EMAIL_INPUT).send_keys(email)
        self.wait_visible(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.REGISTER_BUTTON)
        self.wait_url_contains("/login")
