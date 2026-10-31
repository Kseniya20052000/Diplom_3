from selenium.webdriver.common.by import By

class IngredientModal:
    MODAL_CONTAINER = (By.CSS_SELECTOR, "div.Modal_modal__container__Wo2l_")
    MODAL_TITLE = (By.CSS_SELECTOR, "h2.Modal_modal__title_modified__3Hjkd")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    INGREDIENT_NAME = (By.CSS_SELECTOR, "p.text.text_type_main-medium")
    STATS_LIST = (By.CSS_SELECTOR, "ul.Modal_modal__statsList__6cEm5")
