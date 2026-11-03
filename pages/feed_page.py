import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  # NEW

from pages.base_page import BasePage


class FeedPage(BasePage):

    # Счётчики «Выполнено за всё время» и «Выполнено за сегодня»
    ALL_COUNTERS = (By.CSS_SELECTOR, ".OrderFeed_number__2MbrQ")

    # Заголовки секций статусов
    STATUS_READY_LABEL = (By.XPATH, "//p[contains(text(), 'Готовы:')]")
    STATUS_IN_WORK_LABEL = (By.XPATH, "//p[contains(text(), 'В работе:')]")

    # Список заказов в секции «В работе»
    ORDERS_IN_WORK = (By.CSS_SELECTOR, "ul.OrderFeed_orderList__cBvyi li.text_type_digits-default")

    # блок со статусами «Готовы» и «В работе» — по его тексту ищем номер заказа
    ORDER_STATUS_BOX = (By.CSS_SELECTOR, ".OrderFeed_orderStatusBox__1d4q2")

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

    # получаем текст блока статусов заказов
    @allure.step("Получаем текст блока статусов заказов")
    def get_orders_status_text(self) -> str:
        return self.wait_visible(self.ORDER_STATUS_BOX).text

    # ждём, пока номер заказа появится на ленте (формат с ведущими нулями: 01055)
    @allure.step("Ждём, пока номер заказа появится на ленте")
    def wait_order_number_visible(self, order_number: int, timeout=30) -> str:
        displayed = f"{order_number:05d}"
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: displayed in self.get_orders_status_text())
        return displayed

    # внутренний помощник — текущее значение счётчика по индексу
    def _counter_value(self, index: int) -> int:
        text = self.wait_present_all(self.ALL_COUNTERS)[index].text.strip()
        return int(text) if text.isdigit() else 0

    # ждём, пока счётчик вырастет со значения previous
    @allure.step("Ждём, пока счётчик №{index} вырастет со значения {previous}")
    def wait_counter_increased(self, index: int, previous: int, timeout=60) -> int:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: self._counter_value(index) > previous)
        return self._counter_value(index)
