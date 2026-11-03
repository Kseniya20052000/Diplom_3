import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BasketPage(BasePage):

    BASKET_CONTAINER = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")

    @allure.step("Проверяем, что контейнер корзины отображается")
    def is_basket_visible(self) -> bool:
        return self.wait_visible(self.BASKET_CONTAINER).is_displayed()
