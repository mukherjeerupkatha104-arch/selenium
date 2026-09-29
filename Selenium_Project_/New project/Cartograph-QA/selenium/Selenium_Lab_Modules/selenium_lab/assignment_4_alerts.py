from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.maximize_window()

driver.get("https://the-internet.herokuapp.com/javascript_alerts")

alert_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']")

alert_button.click()
alert = driver.switch_to.alert

print("Alert text:", alert.text)

alert.accept()

print("JavaScript alert accepted successfully")


confirm_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']")

confirm_button.click()
confirm = driver.switch_to.alert

print("Confirm text:", confirm.text)
confirm.dismiss()
print("JavaScript confirm dismissed successfully")
prompt_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']")
prompt_button.click()
prompt = driver.switch_to.alert
print("Prompt text:", prompt.text)
prompt.send_keys("Selenium")
prompt.accept()
print("JavaScript prompt accepted successfully")
with open("reports/assignment_4_report.txt", "w") as file:
    file.write("Assignment 4 - JavaScript Alerts and Confirms\n")
    file.write("Status: PASSED\n")
    file.write("JavaScript Alert: Accepted\n")
    file.write("JavaScript Confirm: Dismissed\n")
    file.write("JavaScript Prompt: Text entered and accepted\n")

print("Assignment 4 PASSED")
print("Report generated successfully.")

driver.quit()