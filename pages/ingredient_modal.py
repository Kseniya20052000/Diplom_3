import allure

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.main_page import MainPage

class IngredientModal(BasePage):
    MODAL_CONTAINER = (By.CSS_SELECTOR, "div.Modal_modal__container__Wo2l_")
    MODAL_TITLE = (By.CSS_SELECTOR, "h2.Modal_modal__title_modified__3Hjkd")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")

    @allure.step("Ожидаем появления модального окна")
    def wait_opened(self):
        self.wait_present(self.MODAL_CONTAINER)
        return self

    @allure.step("Закрываем модалку крестиком")
    def close(self) -> MainPage:
        self.click(self.CLOSE_BUTTON)
        
        main_page = MainPage(self.driver)
        main_page.wait_header_loaded()  
        return main_page

    @allure.step("Получаем заголовок модалки")
    def get_title(self) -> str:
        return self.get_text(self.MODAL_TITLE)