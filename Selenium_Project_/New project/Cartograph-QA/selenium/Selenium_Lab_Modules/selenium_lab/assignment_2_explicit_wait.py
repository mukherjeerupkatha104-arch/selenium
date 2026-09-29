from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.maximize_window()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
start_button = driver.find_element(By.XPATH,"//button[text()='Start']")
start_button.click()
wait = WebDriverWait(driver, 10)
message = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
text = message.text
print("Dynamic text:", text)

try:
    assert text == "Hello World!"

    print("Assignment 2 PASSED")

    with open("reports/assignment_2_report.txt", "w") as file:
        file.write("Assignment 2 - Synchronization & Explicit Waits\n")
        file.write("Status: PASSED\n")
        file.write(f"Dynamic Text: {text}\n")

except AssertionError:

    print("Assignment 2 FAILED")

    with open("reports/assignment_2_report.txt", "w") as file:
        file.write("Assignment 2 - Synchronization & Explicit Waits\n")
        file.write("Status: FAILED\n")
        file.write(f"Dynamic Text: {text}\n")

    raise

driver.quit()