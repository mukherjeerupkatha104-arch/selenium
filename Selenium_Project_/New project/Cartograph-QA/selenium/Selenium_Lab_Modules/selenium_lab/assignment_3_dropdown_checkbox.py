from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

wait = WebDriverWait(driver, 10)

driver.get("https://testautomationpractice.blogspot.com/")

monday = wait.until(EC.presence_of_element_located((By.ID, "monday")))

if not monday.is_selected():
    monday.click()
checkbox_selected = monday.is_selected()

assert checkbox_selected, "Monday checkbox was not selected."

print("Monday checkbox selected successfully")

driver.get("https://jqueryui.com/resources/demos/autocomplete/default.html")

autocomplete = wait.until(EC.visibility_of_element_located((By.ID, "tags")))

autocomplete.send_keys("Ja")

suggestions = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.ui-autocomplete li")))

print("Suggestions found:")

for suggestion in suggestions:
    print(suggestion.text)

    if suggestion.text == "Java":
        suggestion.click()
        break
selected_value = autocomplete.get_attribute("value")

print("Selected value:", selected_value)

assert selected_value == "Java", "Java was not selected."

print("Autocomplete selection successful")
try:
    assert checkbox_selected
    assert selected_value == "Java"

    with open("reports/assignment_3_report.txt", "w") as file:
        file.write("Assignment 3 - Dynamic Dropdowns & Checkboxes\n")
        file.write("Status: PASSED\n")
        file.write("Checkbox: Monday selected\n")
        file.write("Autocomplete: Java selected\n")

    print("Assignment 3 PASSED")
    print("Report generated successfully.")

except AssertionError:

    with open("reports/assignment_3_report.txt", "w") as file:
        file.write("Assignment 3 - Dynamic Dropdowns & Checkboxes\n")
        file.write("Status: FAILED\n")
        file.write(f"Checkbox selected: {checkbox_selected}\n")
        file.write(f"Autocomplete value: {selected_value}\n")

    print("Assignment 3 FAILED")
    raise
driver.quit()