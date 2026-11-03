import allure
import pytest

from pages.main_page import MainPage
from pages.feed_page import FeedPage


@allure.feature("Лента заказов (Feed)")
class TestFeed:

    @allure.title("Проверка: счётчик «Выполнено за всё время» отображается на ленте заказов")
    @pytest.mark.skip(reason="Проверка видимости элемента; изменение значения невозможно без авторизации")
    def test_feed_counter_all_time_visible(self, main_page):
        feed = FeedPage(main_page.driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.close_modal_if_present()
            main_page.wait_header_loaded()
            
        with allure.step("Перейти в раздел «Лента Заказов»"):
            feed.open(main_page.URL)
            main_page.close_modal_if_present()
            main_page.click(main_page.FEED_LINK)

        with allure.step("Дождаться загрузки ленты и получить счётчики"):
            feed.wait_for_counters_loaded()
            counters = feed.get_all_counters()
            assert len(counters) >= 1, "Не найден счётчик «Выполнено за всё время»"

        with allure.step("Прикрепить значение в отчёт и проверить, что оно числовое"):
            value = counters[0].text.strip()
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
        feed = FeedPage(main_page.driver)

        with allure.step("Перейти в раздел «Лента Заказов»"):
            feed.open(main_page.URL)
            main_page.close_modal_if_present()
            main_page.click(main_page.FEED_LINK)

        with allure.step("Дождаться счётчиков и убедиться, что их минимум два"):
            feed.wait_for_counters_loaded()
            counters = feed.get_all_counters()
            assert len(counters) >= 2, "Ожидается минимум 2 счётчика (за всё время и за сегодня)"

        with allure.step("Прикрепить значение «за сегодня» в отчёт и проверить, что оно числовое"):
            value = counters[1].text.strip()
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
        feed = FeedPage(main_page.driver)

        with allure.step("Открыть ленту заказов"):
            feed.open(main_page.URL)
            main_page.close_modal_if_present()
            main_page.click(main_page.FEED_LINK)

        with allure.step("Проверить наличие заголовка «В работе:»"):
            label = feed.wait_visible(feed.STATUS_IN_WORK_LABEL)
            assert "В работе:" in label.text, f"Неверный текст заголовка секции: '{label.text}'"

        with allure.step("Проверить, что список заказов в секции «В работе» присутствует в DOM"):
            orders = feed.wait_present(feed.ORDERS_IN_WORK)
            assert orders is not None, "Список заказов в секции «В работе» не найден"
