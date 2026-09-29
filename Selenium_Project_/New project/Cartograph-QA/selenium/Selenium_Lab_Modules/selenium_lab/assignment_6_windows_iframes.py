from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install())
)

driver.maximize_window()

driver.get("https://the-internet.herokuapp.com/iframe")

iframe = driver.find_element(By.ID, "mce_0_ifr")
driver.switch_to.frame(iframe)
editor = driver.find_element(By.ID, "tinymce")
driver.execute_script("arguments[0].focus();", editor)
editor.send_keys(Keys.CONTROL, "a")
editor.send_keys("Hello from Selenium")

print("Text entered inside iframe successfully")
driver.switch_to.default_content()
print("Switched back to main page successfully")
driver.get("https://the-internet.herokuapp.com/windows")

original_window = driver.current_window_handle
print("Original window:", original_window)
link = driver.find_element(By.LINK_TEXT, "Click Here")
link.click()
windows = driver.window_handles
print("Number of windows:", len(windows))
for window in windows:
    if window != original_window:
        driver.switch_to.window(window)
        break
print("New window title:", driver.title)
assert driver.title == "New Window", \
    "New window title is incorrect."
print("Successfully switched to new window")
driver.close()
print("New window closed")
driver.switch_to.window(original_window)
print("Switched back to original window")
assert driver.current_window_handle == original_window, \
    "Did not return to original window."

print("Returned to original window successfully")
print("--------------------------------")
print("Assignment 6 PASSED")


# Close browser
driver.quit()