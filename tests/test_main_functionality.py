import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Основная функциональность (Main)")
class TestMainFunctionality:

    @allure.title("Переход в Конструктор: проверка появления вкладок")
    @pytest.mark.smoke
    def test_constructor_link_click(self, main_page):
        with allure.step("Перейти в «Лента Заказов», чтобы уйти со страницы конструктора"):
            main_page.go_to_feed()

        with allure.step("Кликнуть по «Конструктор» из ленты заказов"):
            main_page.go_to_constructor()

        with allure.step("Проверить, что появилась активная вкладка «Булки»"):
            active_tab = main_page.get_active_tab_text()
            assert active_tab == "Булки", f"Ожидалась вкладка 'Булки', а найдена: '{active_tab}'"

    @allure.title("Переход по клику на раздел «Лента Заказов»")
    @pytest.mark.smoke
    def test_feed_link_click(self, main_page):
        with allure.step("Перейти в «Лента Заказов»"):
            current_url = main_page.go_to_feed_url()

        with allure.step("Проверить URL страницы ленты"):
            assert "feed" in current_url, f"Ожидался переход в ленту заказов, текущий URL: {current_url}"

    @allure.title("Клик по ингредиенту открывает всплывающее окно с деталями")
    @pytest.mark.smoke
    def test_ingredient_click_opens_modal(self, main_page):
        with allure.step("Открыть модалку ингредиента"):
            modal = main_page.open_first_ingredient_modal()

        with allure.step("Проверить заголовок модального окна"):
            title = modal.get_title()
            assert title == "Детали ингредиента", f"Ожидался заголовок 'Детали ингредиента', а найден: '{title}'"

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    @pytest.mark.smoke
    def test_modal_close_by_cross(self, main_page):
        with allure.step("Открыть модалку ингредиента"):
            modal = main_page.open_first_ingredient_modal()

        with allure.step("Закрыть модалку крестиком"):
            modal.close()

        with allure.step("Убедиться, что модалка исчезла"):
            assert modal.is_closed(), "Модальное окно всё ещё присутствует на странице после закрытия крестиком"

    @allure.title("Счётчик ингредиента увеличивается при добавлении в корзину")
    @pytest.mark.smoke
    def test_ingredient_counter_increases(self, main_page):
        with allure.step("Запомнить значение счётчика булки до добавления"):
            before = main_page.get_first_ingredient_counter()
            allure.attach(str(before), name="Счётчик до добавления", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Перетащить булку в корзину конструктора"):
            main_page.add_first_bun_to_basket()

        with allure.step("Проверить, что счётчик вырос на 2 (булка ставится в два слоя)"):
            after = main_page.get_first_ingredient_counter()
            assert after == before + 2, (
                f"Счётчик булки должен вырасти с {before} до {before + 2}, а он равен {after}"
            )
