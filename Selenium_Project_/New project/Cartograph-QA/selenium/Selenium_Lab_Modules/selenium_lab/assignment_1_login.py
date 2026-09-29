from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("https://www.saucedemo.com/")
username = driver.find_element(By.ID,"user-name")

username.send_keys("standard_user")


password = driver.find_element(By.NAME,"password")

password.send_keys("secret_sauce")


login_button = driver.find_element(By.XPATH,"//input[@id='login-button']")

login_button.click()


current_url = driver.current_url

print("Current URL:", current_url)
try:
    assert "/inventory.html" in current_url

    print("Assignment 1 PASSED")

    with open("reports/assignment_1_report.txt", "w") as file:
        file.write("Assignment 1 - Multi-Locator Challenge\n")
        file.write("Status: PASSED\n")
        file.write(f"URL: {current_url}\n")

except AssertionError:
    print("Assignment 1 FAILED")

    with open("reports/assignment_1_report.txt", "w") as file:
        file.write("Assignment 1 - Multi-Locator Challenge\n")
        file.write("Status: FAILED\n")
        file.write(f"URL: {current_url}\n")

    raise

time.sleep(3)

driver.quit()