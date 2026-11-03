import allure
import pytest

from pages.main_page import MainPage
from pages.feed_page import FeedPage


@allure.feature("Лента заказов (Feed)")
class TestFeed:

    @allure.title("Проверка: счётчик «Выполнено за всё время» отображается на ленте заказов")
    @pytest.mark.skip(reason="Проверка видимости элемента; изменение значения невозможно без авторизации")
    def test_feed_counter_all_time_visible(self, main_page):
        with allure.step("Перейти в раздел «Лента Заказов»"):
            feed = main_page.go_to_feed()

        with allure.step("Дождаться загрузки ленты и получить значения счётчиков"):
            values = feed.get_counter_values()
            assert len(values) >= 1, "Не найден счётчик «Выполнено за всё время»"

        with allure.step("Прикрепить значение в отчёт и проверить, что оно числовое"):
            value = values[0]
            allure.attach(
                value,
                name="Значение «Выполнено за всё время»",
                attachment_type=allure.attachment_type.TEXT
            )
            assert value != "" and value.isdigit(), (
                f"Значение счётчика «Выполнено за всё время» пустое или не является числом: '{value}'"
            )

    @allure.title("Проверка: счётчик «Выполнено за сегодня» отображается на ленте заказов")
    @pytest.mark.skip(reason="Проверка видимости элемента; изменение значения невозможно без авторизации")
    def test_feed_counter_today_visible(self, main_page):
        with allure.step("Перейти в раздел «Лента Заказов»"):
            feed = main_page.go_to_feed()

        with allure.step("Дождаться счётчиков и убедиться, что их минимум два"):
            values = feed.get_counter_values()
            assert len(values) >= 2, "Ожидается минимум 2 счётчика (за всё время и за сегодня)"

        with allure.step("Прикрепить значение «за сегодня» в отчёт и проверить, что оно числовое"):
            value = values[1]
            allure.attach(
                value,
                name="Значение «Выполнено за сегодня»",
                attachment_type=allure.attachment_type.TEXT
            )
            assert value != "" and value.isdigit(), (
                f"Значение счётчика «Выполнено за сегодня» пустое или не является числом: '{value}'"
            )

    @allure.title("Проверка: секция «В работе» присутствует на ленте заказов")
    @pytest.mark.skip(reason="Реальное оформление заказа невозможно без авторизации; тест проверяет наличие секции «В работе»")
    def test_section_in_work_exists(self, main_page):
        with allure.step("Перейти в раздел «Лента Заказов»"):
            feed = main_page.go_to_feed()

        with allure.step("Проверить наличие заголовка «В работе:»"):
            assert feed.is_in_work_section_present(), "Секция «В работе» не найдена на ленте заказов"

        with allure.step("Проверить, что список заказов в секции «В работе» присутствует в DOM"):
            assert feed.is_orders_in_work_list_present(), "Список заказов в секции «В работе» не найден"
