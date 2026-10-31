from selenium.webdriver.common.by import By

class BasketPage:
    BASKET_CONTAINER = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".BurgerConstructor_basket__totalContainer__2Z-ho p.text.text_type_digits-medium")
    BUN_TOP_ITEM = (By.CSS_SELECTOR, ".constructor-element_pos_top")
    BUN_BOTTOM_ITEM = (By.CSS_SELECTOR, ".constructor-element_pos_bottom")
    