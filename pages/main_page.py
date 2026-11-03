import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.feed_page import FeedPage
from pages.ingredient_modal import IngredientModal


class MainPage(BasePage):

    URL = "https://stellarburgers.education-services.ru/"

    # Шапка сайта — признак того, что страница загрузилась
    HEADER = (By.CSS_SELECTOR, "[class*='AppHeader']")

    CONSTRUCTOR_LINK = (By.XPATH, "//p[contains(text(), 'Конструктор')]/parent::a")
    FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")
    INGREDIENTS = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")

    # Локаторы для модальных окон
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")

    # Заголовок конструктора — признак, что мы на нужной странице
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    # Вкладки конструктора
    ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab__1SPyG.tab_tab_type_current__2BEPc span")

    # Корзина конструктора — зона, куда перетаскиваем
    BASKET_AREA = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")
    # Кнопка «Оформить заказ»
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    # Номер заказа в модальном окне
    ORDER_NUMBER = (By.CSS_SELECTOR, "h2.Modal_modal__title_shadow__3ikwq")
    # Счётчик первого ингредиента (булка)
    FIRST_INGREDIENT_COUNTER = (
        By.CSS_SELECTOR,
        "a.BurgerIngredient_ingredient__1TVf6 .counter_counter__num__3nue1",
    )

    @allure.step("Дожидаемся загрузки шапки сайта")
    def wait_header_loaded(self):
        self.wait_visible(self.HEADER)
        return self

    @allure.step("Закрываем модальное окно (если открыто)")
    def close_any_modal(self) -> bool:
        """Закрывает видимую модалку, если она есть. Если нет — ничего не делает."""
        overlays = self.find_visible_elements(self.MODAL_OVERLAY)
        if overlays:
            self.driver.execute_script("arguments[0].click();", overlays[0])
            self.wait_element_hidden(self.MODAL_OVERLAY)
            return True

        close_btns = self.find_visible_elements(self.CLOSE_MODAL_BTN)
        if close_btns:
            self.click(self.CLOSE_MODAL_BTN)
            self.wait_element_hidden(self.MODAL_CONTAINER)
            return True

        return False

    @allure.step("Открываем страницу «Конструктор»")
    def go_to_constructor(self) -> "MainPage":
        self.click(self.CONSTRUCTOR_LINK)
        self.wait_visible(self.CONSTRUCTOR_TITLE)
        return self

    @allure.step("Открываем ленту заказов")
    def go_to_feed(self) -> FeedPage:
        self.click(self.FEED_LINK)
        feed_page = FeedPage(self.driver)
        feed_page.wait_for_counters_loaded()
        return feed_page

    @allure.step("Открываем ленту заказов и возвращаем URL")
    def go_to_feed_url(self) -> str:
        self.click(self.FEED_LINK)
        return self.wait_url_contains("feed")

    @allure.step("Кликаем по первому ингредиенту и открываем его модалку")
    def open_first_ingredient_modal(self) -> IngredientModal:
        self.close_any_modal()
        ingredient = self.wait_clickable(self.INGREDIENTS)
        ingredient.click()
        modal = IngredientModal(self.driver)
        modal.wait_opened()
        return modal

    @allure.step("Получаем текст активной вкладки конструктора")
    def get_active_tab_text(self) -> str:
        return self.wait_visible(self.ACTIVE_TAB).text

    @allure.step("Перетаскиваем первую булку в корзину конструктора")
    def add_first_bun_to_basket(self):
        bun = self.find_visible_elements(self.INGREDIENTS)[0]
        target = self.wait_visible(self.BASKET_AREA)
        self.drag_and_drop(bun, target)
        return self

    @allure.step("Оформляем заказ и возвращаем его номер")
    def create_order(self) -> int:
        self.click(self.ORDER_BUTTON)
        number_text = self.wait_visible(self.ORDER_NUMBER).text.strip()
        order_number = int(number_text)
        self.close_any_modal()
        return order_number

    @allure.step("Получаем счётчик первого ингредиента")
    def get_first_ingredient_counter(self) -> int:
        text = self.wait_visible(self.FIRST_INGREDIENT_COUNTER).text.strip()
        return int(text) if text.isdigit() else 0
