import allure
import pytest

from pages.feed_page import FeedPage


@allure.feature("Лента заказов (Feed)")
class TestFeed:

    @allure.title("Счётчик «Выполнено за всё время» увеличивается после оформления заказа")
    def test_feed_counter_all_time_increases(self, driver, logged_in_main_page):
        main = logged_in_main_page

        with allure.step("Перейти в ленту заказов и запомнить значение счётчика"):
            main.click_feed_link()
            feed = FeedPage(driver)
            feed.wait_for_counters_loaded()

            values = feed.get_counter_values()
            assert len(values) >= 1 and values[0].isdigit(), "Счётчик «Выполнено за всё время» не найден"
            before = int(values[0])
            allure.attach(str(before), name="Счётчик до заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Вернуться в конструктор, перетащить булку и оформить заказ"):
            main.go_to_constructor()
            main.add_first_bun_to_basket()
            order_number = main.create_order()
            allure.attach(str(order_number), name="Номер заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Вернуться в ленту и дождаться, когда счётчик вырастет"):
            main.click_feed_link()
            feed = FeedPage(driver)
            feed.wait_for_counters_loaded()

            after = feed.wait_counter_increased(0, before, timeout=60)
            assert after > before, (
                f"Счётчик «Выполнено за всё время» должен вырасти с {before}, а он равен {after}"
            )

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после оформления заказа")
    def test_feed_counter_today_increases(self, driver, logged_in_main_page):
        main = logged_in_main_page

        with allure.step("Перейти в ленту заказов и запомнить значение счётчика"):
            main.click_feed_link()
            feed = FeedPage(driver)
            feed.wait_for_counters_loaded()

            values = feed.get_counter_values()
            assert len(values) >= 2 and values[1].isdigit(), "Счётчик «Выполнено за сегодня» не найден"
            before = int(values[1])
            allure.attach(str(before), name="Счётчик до заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Вернуться в конструктор, перетащить булку и оформить заказ"):
            main.go_to_constructor()
            main.add_first_bun_to_basket()
            order_number = main.create_order()
            allure.attach(str(order_number), name="Номер заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Вернуться в ленту и дождаться, когда счётчик вырастет"):
            main.click_feed_link()
            feed = FeedPage(driver)
            feed.wait_for_counters_loaded()

            after = feed.wait_counter_increased(1, before, timeout=60)
            assert after > before, (
                f"Счётчик «Выполнено за сегодня» должен вырасти с {before}, а он равен {after}"
            )

    @allure.title("Оформленный заказ появляется в разделе «В работе»")
    def test_order_appears_in_feed(self, driver, logged_in_main_page):
        main = logged_in_main_page

        with allure.step("Перетащить булку и оформить заказ"):
            main.add_first_bun_to_basket()
            order_number = main.create_order()
            allure.attach(str(order_number), name="Номер заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Перейти в ленту и дождаться появления заказа в разделе «В работе»"):
            main.click_feed_link()
            feed = FeedPage(driver)

        with allure.step("Проверить, что номер заказа найден в списке «В работе»"):
            found = feed.wait_order_number_in_work(order_number, timeout=45)
            assert found, f"Заказ №{order_number} не появился в списке «В работе» за отведённое время"
