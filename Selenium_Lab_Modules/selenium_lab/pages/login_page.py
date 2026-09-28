from selenium.webdriver.common.by import By


class LoginPage:

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()