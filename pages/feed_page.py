import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FeedPage(BasePage):

    # Счётчики «Выполнено за всё время» и «Выполнено за сегодня»
    ALL_COUNTERS = (By.CSS_SELECTOR, ".OrderFeed_number__2MbrQ")

    # Заголовки секций статусов
    STATUS_READY_LABEL = (By.XPATH, "//p[contains(text(), 'Готовы:')]")
    STATUS_IN_WORK_LABEL = (By.XPATH, "//p[contains(text(), 'В работе:')]")

    # Список заказов в секции «В работе»
    ORDERS_IN_WORK = (By.CSS_SELECTOR, "ul.OrderFeed_orderList__cBvyi li.text_type_digits-default")

    @allure.step("Ждём загрузки счётчиков на ленте заказов")
    def wait_for_counters_loaded(self):
        self.wait_visible(self.ALL_COUNTERS)
        return self

    @allure.step("Получаем значения счётчиков (список строк)")
    def get_counter_values(self) -> list[str]:
        elements = self.wait_present_all(self.ALL_COUNTERS)
        return [el.text.strip() for el in elements]

    @allure.step("Проверяем, что секция «В работе» присутствует")
    def is_in_work_section_present(self) -> bool:
        self.wait_visible(self.STATUS_IN_WORK_LABEL)
        return True

    @allure.step("Проверяем, что список заказов в секции «В работе» присутствует")
    def is_orders_in_work_list_present(self) -> bool:
        self.wait_present(self.ORDERS_IN_WORK)
        return True
