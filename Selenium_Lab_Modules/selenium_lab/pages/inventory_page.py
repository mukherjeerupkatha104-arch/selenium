from selenium.webdriver.common.by import By


class InventoryPage:

    PRODUCTS_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return self.driver.find_element(*self.PRODUCTS_TITLE).text