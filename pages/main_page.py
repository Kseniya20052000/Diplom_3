import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.ingredient_modal import IngredientModal
from pages.feed_page import FeedPage

class MainPage(BasePage):
    URL = "https://stellarburgers.education-services.ru/"

    HEADER = (By.CSS_SELECTOR, "[class*='AppHeader']")
    CONSTRUCTOR_LINK = (By.XPATH, "//p[contains(text(), 'Конструктор')]/parent::a")
    FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")
    INGREDIENTS = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")

    MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")
    MODAL_TITLE = (By.CSS_SELECTOR, "h2.Modal_modal__title_modified__3Hjkd")

    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")
    TABS_CONTAINER = (By.CSS_SELECTOR, "div[style*='display: flex;']")
    ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab__1SPyG.tab_tab_type_current__2BEPc span")

    @allure.step("Дожидаемся загрузки шапки сайта")
    def wait_header_loaded(self):
        self.wait_visible(self.HEADER)
        return self

    @allure.step("Закрываем модальное окно (если открыто)")
    def close_any_modal(self) -> bool:
        # Сначала пробуем кликнуть по оверлею
        overlays = self.find_elements(self.MODAL_OVERLAY)
        if overlays:
            self.driver.execute_script("arguments[0].click();", overlays[0])
            self.wait_elements_gone(self.MODAL_OVERLAY)
            return True

        # Потом по кнопке закрытия
        close_btns = self.find_elements(self.CLOSE_MODAL_BTN)
        if close_btns:
            self.click(self.CLOSE_MODAL_BTN)  # BasePage.click уже умеет ждать и делать JS-клик
            self.wait_elements_gone(self.MODAL_CONTAINER)
            return True

        return False

    @allure.step("Открываем страницу «Конструктор»")
    def go_to_constructor(self) -> "MainPage":
        self.click(self.CONSTRUCTOR_LINK)
        self.wait_visible(self.CONSTRUCTOR_TITLE)
        return self

    @allure.step("Открываем ленту заказов")
    def go_to_feed(self) -> "FeedPage":
        from pages.feed_page import FeedPage  # избегаем циклического импорта
        self.click(self.FEED_LINK)
        feed_page = FeedPage(self.driver)
        feed_page.wait_for_counters_loaded()
        return feed_page

    @allure.step("Кликаем по первому ингредиенту и открываем его модалку")
    def open_first_ingredient_modal(self) -> "IngredientModal":
        self.close_any_modal()
        ingredient = self.wait_clickable(self.INGREDIENTS)
        ingredient.click()
        modal = IngredientModal(self.driver)
        modal.wait_opened()
        return modal
