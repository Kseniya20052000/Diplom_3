import pytest
import allure

from pages.user_helpers import generate_unique_email, get_default_password, get_default_name
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
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
    page = MainPage(driver)

    with allure.step("Открыть главную страницу"):
        page.open()

    with allure.step("Закрыть модальное окно, если оно открыто"):
        page.close_any_modal()

    with allure.step("Дождаться, что модальное окно закрыто"):
        page.wait_element_hidden(page.MODAL_OVERLAY)

    return page


@pytest.fixture
def logged_in_main_page(driver, main_page):
    email = generate_unique_email()
    password = get_default_password()
    name = get_default_name()

    with allure.step(f"Открыть личный кабинет и перейти к регистрации ({email})"):
        main_page.click_account_link()
        login_page = LoginPage(driver)
        login_page.wait_visible(LoginPage.EMAIL_INPUT)

        login_page.click_register_link()
        register_page = RegisterPage(driver)
        register_page.wait_visible(RegisterPage.NAME_INPUT)

        register_page.register(name, email, password)

    with allure.step("Войти под новым пользователем"):
        login_page_after_register = LoginPage(driver)
        login_page_after_register.wait_visible(LoginPage.EMAIL_INPUT)
        login_page_after_register.login(email, password)

    with allure.step("Дождаться загрузки конструктора после входа"):
        main_page.wait_header_loaded()
        main_page.close_any_modal()

    return main_page
