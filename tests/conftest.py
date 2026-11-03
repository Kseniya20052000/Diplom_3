import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.main_page import MainPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    allure.attach(
        browser,
        name="Запускаемый браузер",
        attachment_type=allure.attachment_type.TEXT,
    )

    if browser == "chrome":
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)

    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
@allure.title("Подготовка MainPage: открытие, закрытие модалки, ожидание шапки")
def main_page(driver):
    """
    Базовая подготовка для тестов, которые стартуют с главной страницы.
    Гарантирует, что страница открыта, модалка закрыта, шапка загружена.
    Возвращает готовый экземпляр MainPage.
    """
    page = MainPage(driver)

    with allure.step("Открыть главную страницу"):
        page.open()

    with allure.step("Закрыть модальное окно, если оно открыто"):
        page.close_any_modal()

    with allure.step("Дождаться загрузки шапки сайта"):
        page.wait_header_loaded()

    return page
