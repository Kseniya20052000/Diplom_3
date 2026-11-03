import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FeedPage(BasePage):
    ALL_COUNTERS = (By.CSS_SELECTOR, ".OrderFeed_number__2MbrQ")
    STATUS_READY_LABEL = (By.XPATH, "//p[contains(text(), 'Готовы:')]")
    STATUS_IN_WORK_LABEL = (By.XPATH, "//p[contains(text(), 'В работе:')]")
    ORDERS_IN_WORK = (By.CSS_SELECTOR, "ul.OrderFeed_orderList__cBvyi li.text_type_digits-default")

    @allure.step("Ждём загрузки счётчиков на ленте заказов")
    def wait_for_counters_loaded(self):
        self.wait_visible(self.ALL_COUNTERS)
        return self

    @allure.step("Получаем значения счётчиков (список текстов)")
    def get_counters_texts(self) -> list[str]:
        elements = self.wait_present_all(self.ALL_COUNTERS)  # нужно добавить в BasePage wait_present_all
        return [el.text for el in elements]

    @allure.step("Проверяем, что секция «В работе» присутствует")
    def is_in_work_section_present(self) -> bool:
        try:
            self.wait_visible(self.STATUS_IN_WORK_LABEL)
            return True
        except Exception:
            return False