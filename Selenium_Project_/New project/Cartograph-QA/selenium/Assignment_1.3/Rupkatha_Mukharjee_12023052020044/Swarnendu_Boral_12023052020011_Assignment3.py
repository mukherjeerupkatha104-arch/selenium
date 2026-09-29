
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/login")

# 1)CSS Selector - Username
user = driver.find_element(By.CSS_SELECTOR, "#username")
user.send_keys("tomsmith")
print("Username:", user.get_attribute("id"))

# 2) CSS Selector - Password
password = driver.find_element(By.CSS_SELECTOR, "#password")
password.send_keys("SuperSecretPassword!")
print("Password:", password.get_attribute("id"))

# 3)CSS Selector - Login button
button = driver.find_element(By.CSS_SELECTOR, "button.radius")
print("Button:", button.text)

# 4)CSS Wildcard Selector - ID starts with "user_"
elements = driver.find_elements(By.CSS_SELECTOR, "[id^='user_']")

print("Elements with ID starting with user_:", len(elements))

for element in elements:
    print(element.get_attribute("id"))

driver.quit()

