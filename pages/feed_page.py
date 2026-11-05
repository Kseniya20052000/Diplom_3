import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FeedPage(BasePage):

    ALL_COUNTERS = (By.CSS_SELECTOR, ".OrderFeed_number__2MbrQ")

    STATUS_READY_LABEL = (By.XPATH, "//p[contains(text(), 'Готовы:')]")
    STATUS_IN_WORK_LABEL = (By.XPATH, "//p[contains(text(), 'В работе:')]")

    ORDERS_IN_WORK = (By.CSS_SELECTOR, "ul.OrderFeed_orderList__cBvyi li.text_type_digits-default")

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

    @allure.step("Получаем текст блока статусов заказов")
    def get_orders_status_text(self) -> str:
        return self.wait_visible(self.ORDER_STATUS_BOX).text

    @allure.step("Ждём появления номера заказа в списке «В работе»")
    def wait_order_number_in_work(self, order_number: str, timeout: int = 45) -> bool:
        expected = int(order_number)

        def order_in_work(_):
            items = self.find_elements(self.ORDERS_IN_WORK)
            for item in items:
                text = (item.get_attribute("textContent") or "").strip()
                if text.isdigit() and int(text) == expected:
                    return True
            return False

        found = self.wait_until(order_in_work, timeout=timeout, poll_frequency=2)
        allure.attach(
            f"Искали заказ {order_number} в списке «В работе»: {'найден' if found else 'не найден'}",
            name="Результат поиска заказа",
            attachment_type=allure.attachment_type.TEXT,
        )
        return found

    @allure.step("Читаем значение счётчика №{index}")
    def _counter_value(self, index: int) -> int:
        text = self.wait_present_all(self.ALL_COUNTERS)[index].text.strip()
        return int(text) if text.isdigit() else 0

    @allure.step("Ждём, пока счётчик №{index} вырастет со значения {previous}")
    def wait_counter_increased(self, index: int, previous: int, timeout=60) -> int:
        self.wait_until(lambda d: self._counter_value(index) > previous, timeout=timeout)
        return self._counter_value(index)
