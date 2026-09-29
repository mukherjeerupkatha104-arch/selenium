import sys
import os
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.saucedemo.com/")
login_page = LoginPage(driver)
login_page.login("standard_user","secret_sauce")
print("Login completed successfully")
inventory_page = InventoryPage(driver)
page_title = inventory_page.get_page_title()
print("Inventory page title:", page_title)
try:

    
    assert "/inventory.html" in driver.current_url

    
    assert page_title == "Products"

    print("POM login test PASSED")


    
    
    

    with open(
        os.path.join(
            project_folder,
            "reports",
            "assignment_7_report.txt"
        ),
        "w"
    ) as file:

        file.write("Assignment 7 - Page Object Model (POM)\n")
        file.write("Status: PASSED\n")
        file.write("Login: Successful\n")
        file.write("Inventory Page: Reached successfully\n")
        file.write("Page Title: Products\n")
        file.write("Page Object Model: Implemented successfully\n")
        file.write("Assertions: Passed\n")

    print("Report generated successfully.")


except AssertionError:

    print("POM login test FAILED")


    
    
    

    with open(
        os.path.join(
            project_folder,
            "reports",
            "assignment_7_report.txt"
        ),
        "w"
    ) as file:

        file.write("Assignment 7 - Page Object Model (POM)\n")
        file.write("Status: FAILED\n")
        file.write(f"Current URL: {driver.current_url}\n")
        file.write(f"Page Title: {page_title}\n")

    print("Failure report generated.")

    raise



driver.quit()