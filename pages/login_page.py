import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://stellarburgers.education-services.ru/login"

    EMAIL_INPUT = (By.XPATH, "//fieldset[.//label[text()='Email']]//input")
    PASSWORD_INPUT = (By.XPATH, "//fieldset[.//label[text()='Пароль']]//input")

    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/register']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")

    @allure.step("Кликаем по ссылке «Зарегистрироваться»")
    def click_register_link(self):
        self.click(self.REGISTER_LINK)

    @allure.step("Входим под пользователем: {email}")
    def login(self, email: str, password: str):
        self.wait_visible(self.EMAIL_INPUT).send_keys(email)
        self.wait_visible(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)
