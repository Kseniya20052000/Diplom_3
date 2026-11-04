import pytest
import allure

from pages.user_helpers import generate_unique_email, get_default_password, get_default_name
from pages.main_page import MainPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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

    with allure.step("Дождаться, что модальное окно закрыто"):
        page.wait_element_hidden(page.MODAL_OVERLAY)

    return page


@pytest.fixture
def logged_in_main_page(main_page):
    """
    Регистрирует уникального пользователя через UI, входит в аккаунт
    и возвращает главную страницу под залогиненным пользователем.
    Зависит от main_page: тест стартует с уже открытой главной.
    """
    email = generate_unique_email()
    password = get_default_password()
    name = get_default_name()

    with allure.step(f"Зарегистрировать пользователя {email}"):
        login_page = main_page.open_account()
        register_page = login_page.go_to_register()
        login_page = register_page.register(name, email, password)

    with allure.step("Войти под новым пользователем"):
        login_page.login(email, password)

    with allure.step("Дождаться загрузки конструктора после входа"):
        main_page.wait_header_loaded()
        main_page.close_any_modal()

    return main_page
