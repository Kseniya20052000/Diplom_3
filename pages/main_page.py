import allure

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)

from pages.base_page import BasePage
from pages.feed_page import FeedPage
from pages.ingredient_modal import IngredientModal
from pages.login_page import LoginPage


class MainPage(BasePage):

    URL = "https://stellarburgers.education-services.ru/"

    HEADER = (By.CSS_SELECTOR, "[class*='AppHeader']")

    CONSTRUCTOR_LINK = (By.XPATH, "//p[contains(text(), 'Конструктор')]/parent::a")
    FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")
    INGREDIENTS = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")

    MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")

    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab__1SPyG.tab_tab_type_current__2BEPc span")

    BASKET_AREA = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")

    ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/account']")

    BUN_IN_BASKET = (
        By.XPATH,
        "//div[contains(@class,'constructor-element_pos_top') and not(contains(., 'Перетяните'))]",
    )

    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER = (By.CSS_SELECTOR, "h2.Modal_modal__title_shadow__3ikwq")
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
        if self.find_visible_elements(self.CLOSE_MODAL_BTN):
            self.click(self.CLOSE_MODAL_BTN)
            self.wait_modal_closed()
            return True

        overlays = self.find_visible_elements(self.MODAL_OVERLAY)
        if overlays:
            self.js_click(overlays[0])
            self.wait_modal_closed()
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
        last_error = None
        for attempt in range(3):
            self.close_any_modal()
            try:
                ingredient = self.wait_clickable(self.INGREDIENTS)
                ingredient.click()
                modal = IngredientModal(self.driver)
                modal.wait_opened()
                return modal
            except ElementClickInterceptedException as e:
                last_error = e
                allure.attach(
                    f"Попытка {attempt + 1}: клик перехвачен оверлеем, закрываем модалку и пробуем снова",
                    name="Клик перехвачен",
                    attachment_type=allure.attachment_type.TEXT,
                )

        ingredient = self.wait_clickable(self.INGREDIENTS)
        self.js_click(ingredient)
        modal = IngredientModal(self.driver)
        modal.wait_opened()
        return modal

    @allure.step("Получаем текст активной вкладки конструктора")
    def get_active_tab_text(self) -> str:
        return self.wait_visible(self.ACTIVE_TAB).text

    @allure.step("Проверяем, что булка находится в корзине")
    def is_bun_in_basket(self) -> bool:
        return bool(self.find_visible_elements(self.BUN_IN_BASKET))

    @allure.step("Перетаскиваем булку в корзину конструктора (с проверкой результата)")
    def add_first_bun_to_basket(self, attempts: int = 3):
        if self.is_bun_in_basket():
            return self

        for attempt in range(1, attempts + 1):
            bun = self.wait_visible(self.INGREDIENTS)
            target = self.wait_visible(self.BASKET_AREA)
            self.drag_and_drop(bun, target)

            try:
                self.wait_visible(self.BUN_IN_BASKET)
                return self
            except TimeoutException:
                allure.attach(
                    f"Попытка {attempt}: булка не попала в корзину, пробуем снова",
                    name="Drag не сработал",
                    attachment_type=allure.attachment_type.TEXT,
                )

        raise TimeoutException(
            "Булку не удалось перетащить в корзину за 3 попытки — проверь локаторы и сценарий drag"
        )

    @allure.step("Оформляем заказ и возвращаем его номер")
    def create_order(self) -> int:
        if not self.is_bun_in_basket():
            self.add_first_bun_to_basket()

        self.click(self.ORDER_BUTTON)
        number_text = self.wait_visible(self.ORDER_NUMBER).text.strip()
        order_number = int(number_text)
        self.close_any_modal()
        return order_number

    @allure.step("Получаем счётчик первого ингредиента")
    def get_first_ingredient_counter(self) -> int:
        text = self.wait_visible(self.FIRST_INGREDIENT_COUNTER).text.strip()
        return int(text) if text.isdigit() else 0

    @allure.step("Открываем «Личный Кабинет»")
    def open_account(self):
        from pages.login_page import LoginPage
        self.click(self.ACCOUNT_LINK)
        login_page = LoginPage(self.driver)
        login_page.wait_visible(LoginPage.EMAIL_INPUT)
        return login_page

    @allure.step("Дожидаемся, что оверлей модального окна перестал перекрывать страницу")
    def wait_modal_closed(self, timeout: int = 15):
        def overlay_gone(_):
            overlays = self.find_elements(self.MODAL_OVERLAY)
            return not overlays or all(not o.is_displayed() for o in overlays)

        self.wait_until(overlay_gone, timeout=timeout)
        return self
