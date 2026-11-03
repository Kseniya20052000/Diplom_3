import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс страниц. Единственное место, где напрямую используется драйвер."""

    URL = "https://stellarburgers.education-services.ru/"

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Навигация ---

    @allure.step("Открываем страницу: {url}")
    def open(self, url=None):
        self.driver.get(url if url is not None else self.URL)

    @allure.step("Проверяем, что в URL есть фрагмент: {fragment}")
    def wait_url_contains(self, fragment):
        self.wait.until(lambda d: fragment in d.current_url)
        return self.driver.current_url

    # --- Ожидания и поиск элементов ---

    @allure.step("Ожидаем видимости элемента: {locator}")
    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидаем кликабельности элемента: {locator}")
    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Ожидаем присутствия элемента: {locator}")
    def wait_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Ожидаем присутствия всех элементов: {locator}")
    def wait_present_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Ждём, пока элементов не останется: {locator}")
    def wait_elements_gone(self, locator):
        return self.wait.until(lambda d: len(d.find_elements(*locator)) == 0)

    @allure.step("Ищем элементы: {locator}")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    # --- Действия ---

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        """Клик с прокруткой и JS-фолбэком — помогает, если элемент почти виден."""
        element = self.wait_clickable(locator)
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

    @allure.step("Получаем текст элемента: {locator}")
    def get_text(self, locator):
        return self.wait_visible(locator).text
