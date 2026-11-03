import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:

    URL = "https://stellarburgers.education-services.ru/"

    CONSTRUCTOR_LINK = (By.XPATH, "//p[contains(text(), 'Конструктор')]/parent::a")
    FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")
    INGREDIENTS = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")

    # Локаторы для модальных окон (нужны только как страховка при открытии страницы)
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")

    # Вкладки конструктора (для проверки перехода)
    TABS_CONTAINER = (By.CSS_SELECTOR, "div[style*='display: flex;']")
    ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab__1SPyG.tab_tab_type_current__2BEPc span")

    # Заголовок конструктора — однозначный признак, что мы на нужной странице
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Клик по элементу: {locator}")
    def safe_click(self, locator):
        """Клик с прокруткой и JS-фолбэком — помогает, если элемент почти виден."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        try:
            element.click()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Закрываем модальное окно, если оно открыто")
    def close_modal_if_present(self):
        """
        Тихо закрывает модалку/оверлей, если он есть.
        Если нет — просто ничего не делает.
        """
        # Сначала пробуем кликнуть по оверлею (серый фон)
        overlays = self.driver.find_elements(*self.MODAL_OVERLAY)
        if overlays:
            try:
                overlays[0].click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", overlays[0])
            # Ждём, пока оверлей исчезнет
            try:
                self.wait.until(lambda d: len(d.find_elements(*self.MODAL_OVERLAY)) == 0)
            except Exception:
                pass
            return True

        # Потом пробуем крестик
        close_btns = self.driver.find_elements(*self.CLOSE_MODAL_BTN)
        if close_btns:
            try:
                close_btns[0].click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", close_btns[0])
            try:
                self.wait.until(lambda d: len(d.find_elements(*self.MODAL_CONTAINER)) == 0)
            except Exception:
                pass
            return True

        return False

    @allure.step("Открываем модальное окно ингредиента")
    def open_ingredient_modal(self):
        # Страховка: убираем любую мешающую модалку перед кликом
        self.close_modal_if_present()

        ingredients = self.wait.until(EC.presence_of_all_elements_located(self.INGREDIENTS))
        ingredient = ingredients[0]
        ingredient.click()
        # Ждём появления модального окна
        self.wait.until(lambda d: len(d.find_elements(*self.MODAL_CONTAINER)) > 0)
