import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FeedPage:

    ALL_TIME_COUNTER = (By.CSS_SELECTOR, ".OrderFeed_number__2MbrQ")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button.button_button__33qZ0.button_button_type_primary__1O7Bx")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Получаем все счётчики заказов на ленте")
    def get_all_counters(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.ALL_TIME_COUNTER))

    @allure.step("Кликаем по кнопке «Оформить заказ»")
    def click_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        btn.click()

    @allure.step("Ожидаем загрузки счётчиков на ленте заказов")
    def wait_for_counters_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.ALL_TIME_COUNTER))
