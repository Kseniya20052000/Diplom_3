import allure
import pytest

from pages.main_page import MainPage
from pages.ingredient_modal import IngredientModal
from pages.basket_page import BasketPage


@allure.feature("Основная функциональность (Main)")
class TestMainFunctionality:

    @allure.title("Переход в Конструктор: проверка появления вкладок")
    @pytest.mark.smoke
    def test_constructor_link_click(self, main_page):

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.close_modal_if_present()
            main_page.wait_header_loaded()

        with allure.step("Перейти в «Лента Заказов», чтобы уйти со страницы конструктора"):
            main_page.click(main_page.FEED_LINK)
            main_page.wait_url_contains("feed")

        with allure.step("Кликнуть по «Конструктор» из ленты заказов"):
            main_page.click(main_page.CONSTRUCTOR_LINK)

        with allure.step("Дождаться заголовка конструктора «Соберите бургер»"):
            main_page.wait_visible(main_page.CONSTRUCTOR_TITLE)

        with allure.step("Проверить, что появилась активная вкладка «Булки»"):
            active_tab = main_page.wait_visible(main_page.ACTIVE_TAB)
            assert active_tab.text == "Булки", f"Ожидалась вкладка 'Булки', а найдена: '{active_tab.text}'"

    @allure.title("Переход по клику на раздел «Лента Заказов»")
    @pytest.mark.smoke
    def test_feed_link_click(self, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.close_modal_if_present()

        with allure.step("Кликнуть по «Лента Заказов»"):
            main_page.click(main_page.FEED_LINK)

        with allure.step("Дождаться перехода на страницу ленты и проверить URL"):
            current_url = main_page.wait_url_contains("feed")
            assert "feed" in current_url, f"Ожидался переход в ленту заказов, текущий URL: {current_url}"

    @allure.title("Клик по ингредиенту открывает всплывающее окно с деталями")
    @pytest.mark.smoke
    def test_ingredient_click_opens_modal(self, main_page):
        modal = IngredientModal(main_page.driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.close_modal_if_present()

        with allure.step("Кликнуть по любому ингредиенту"):
            ingredients = main_page.wait_present(main_page.INGREDIENTS)
            ingredients[0].click()

        with allure.step("Дождаться появления модального окна"):
            modal.wait_opened()

        with allure.step("Проверить заголовок модального окна"):
            title = main_page.wait_visible(modal.MODAL_TITLE)
            assert title.text == "Детали ингредиента", f"Ожидался заголовок 'Детали ингредиента', а найден: '{title.text}'"

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    @pytest.mark.smoke
    def test_modal_close_by_cross(self, main_page):
        modal = IngredientModal(main_page.driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.close_modal_if_present()

        with allure.step("Открыть модалку через клик по ингредиенту"):
            main_page.open_ingredient_modal()

        with allure.step("Закрыть модалку крестиком"):
            modal.close()

        with allure.step("Убедиться, что модалка исчезла"):
            assert modal.is_closed(), "Модальное окно всё ещё присутствует на странице после закрытия крестиком"

    @allure.title("Проверка отображения корзины (счётчики недоступны из-за стенда)")
    @pytest.mark.skip(reason="Стенд временно недоступен из-за внешних инцидентов; проверка счётчика невозможна без реальной авторизации и бэкенда")
    def test_basket_counter_increases_on_add(self, main_page):
        basket = BasketPage(main_page.driver)

        with allure.step("Открыть главную страницу"):
            basket.open(main_page.URL)

        with allure.step("Дождаться и проверить, что контейнер корзины отображается"):
            basket_container = basket.wait_visible(basket.BASKET_CONTAINER)
            assert basket_container.is_displayed(), "Контейнер корзины не отображается на странице"
