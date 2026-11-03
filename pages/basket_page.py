import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BasketPage(BasePage):

    BASKET_CONTAINER = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")

    @allure.step("Ожидаем присутствия всех элементов: {locator}")
    def wait_present_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))