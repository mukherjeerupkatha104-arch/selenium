
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/login")

# we locate the button using a CSS child selector
button = driver.find_element(By.CSS_SELECTOR,"form#login button")

print("Button text:", button.text)

# for interaction with the button
button.click()

driver.quit()

