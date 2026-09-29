
import sys
import os
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pytest_html import extras
@pytest.fixture
def driver():

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    browser.maximize_window()

    browser.get("https://www.saucedemo.com/")

    yield browser

    browser.quit()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            
            screenshot_folder = os.path.join(project_folder,"reports","screenshots")

            os.makedirs(screenshot_folder,exist_ok=True)

            
            screenshot_path = os.path.join(screenshot_folder,f"{item.name}.png")

            
            driver.save_screenshot(screenshot_path)

            print(f"\nScreenshot saved: {screenshot_path}")

            
            screenshot = driver.get_screenshot_as_png()

            
            extra = getattr(report,"extras",)

            extra.append(extras.image(screenshot,mime_type="image/png"))

            report.extras = extra

def test_valid_login(driver):

    login_page = LoginPage(driver)

    login_page.login("standard_user","secret_sauce")

    assert "/inventory.html" in driver.current_url
def test_invalid_password(driver):

    login_page = LoginPage(driver)

    login_page.login("standard_user","wrong_password")

    assert "/inventory.html" not in driver.current_url
def test_invalid_username(driver):

    login_page = LoginPage(driver)

    login_page.login("wrong_user","secret_sauce")

    assert "/inventory.html" not in driver.current_url
    








