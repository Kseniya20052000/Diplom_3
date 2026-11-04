import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait   

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

    # ждём, пока цифры номера заказа появятся в блоке статусов ленты
    @allure.step("Ждём появления номера заказа в ленте")
    def wait_order_number_visible(self, order_number: str, timeout: int = 45) -> str:
        """Ждёт, пока заказ с номером появится в списках ленты.
        Сравнение нормализованное: '01389' и '1389' считаются одинаковым номером."""
        expected = int(order_number)  # убираем ведущие нули раз и навсегда
        wait = WebDriverWait(self.driver, timeout, poll_frequency=2)


        def order_found(driver):
            items = driver.find_elements(By.CSS_SELECTOR, "ul[class*='OrderFeed_orderList'] li")
            for item in items:
                # textContent берётся из DOM напрямую — Chrome отдаёт его
                # даже для элементов вне вьюпорта, без скроллов и пауз
                text = (item.get_attribute("textContent") or "").strip()
                if text.isdigit() and int(text) == expected:
                    return text
            return False

        found = wait.until(order_found)
        allure.attach(
            f"Искали: {order_number}, нашли в ленте: {found}",
            name="Номер заказа найден",
            attachment_type=allure.attachment_type.TEXT,
        )
        return found


        def order_found(driver):
            try:
                # Находим все элементы с номерами заказов
                items = driver.find_elements(*ORDER_LIST_ITEMS)
                # Проверяем, есть ли среди них нужный номер
                for item in items:
                    if item.text.strip() == order_number:
                        return item
                return False
            except Exception:
                return False

        found_element = wait.until(order_found)
        allure.attach(found_element.text, name="Найденный номер заказа в ленте", attachment_type=allure.attachment_type.TEXT)
        return found_element.text


    # внутренний помощник — текущее значение счётчика по индексу
    def _counter_value(self, index: int) -> int:
        text = self.wait_present_all(self.ALL_COUNTERS)[index].text.strip()
        return int(text) if text.isdigit() else 0

    # ждём, пока счётчик вырастет 
    @allure.step("Ждём, пока счётчик №{index} вырастет со значения {previous}")
    def wait_counter_increased(self, index: int, previous: int, timeout=60) -> int:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: self._counter_value(index) > previous)
        return self._counter_value(index)
