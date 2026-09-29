from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/login")

# 1) By.ID - Username
user = driver.find_element(By.ID, "username")
user.send_keys("tomsmith")
print("Username:", user.get_attribute("id"))

# 2) By.NAME - Password
password = driver.find_element(By.NAME, "password")
password.send_keys("SuperSecretPassword!")
print("Password:", password.get_attribute("name"))

# 3) By.TAG_NAME - Heading
heading = driver.find_element(By.TAG_NAME, "h2")
print("Heading:", heading.text)

# 4) By.LINK_TEXT - Link
link = driver.find_element(By.LINK_TEXT, "Elemental Selenium")
print("Link:", link.text)

# 5) By.CLASS_NAME - Login Button
button = driver.find_element(By.CLASS_NAME, "radius")
print("Button:", button.text)
time.sleep(3)

driver.quit()