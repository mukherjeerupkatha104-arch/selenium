import sys
import os
import csv
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
csv_file = os.path.join(
    project_folder,
    "data",
    "login_data.csv"
)
test_data = []
with open(csv_file, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        test_data.append(row)
print("Number of test cases:", len(test_data))
report_file = os.path.join(project_folder,"reports","assignment_8_report.txt")
with open(report_file, "w") as report:

    report.write("Assignment 8 - Data-Driven Automation\n")
    report.write("=====================================\n\n")
for index, data in enumerate(test_data, start=1):

    username = data["username"]
    password = data["password"]
    expected_result = data["expected_result"]

    print("--------------------------------")
    print("Test Case:", index)
    print("Username:", username)
    print("Expected Result:", expected_result)


    
    
    

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        )
    )

    driver.maximize_window()

    driver.get("https://www.saucedemo.com/")


    
    
    

    login_page = LoginPage(driver)

    login_page.login(
        username,
        password
    )


    
    
    

    if expected_result == "success":

        actual_result = "success"

        try:

            assert "/inventory.html" in driver.current_url

            test_status = "PASSED"

            print("Result: SUCCESS")
            print("Test Case PASSED")

        except AssertionError:

            actual_result = "error"
            test_status = "FAILED"

            print("Result: ERROR")
            print("Test Case FAILED")


    else:

        actual_result = "error"

        try:

            assert "/inventory.html" not in driver.current_url

            test_status = "PASSED"

            print("Result: ERROR")
            print("Test Case PASSED")

        except AssertionError:

            actual_result = "success"
            test_status = "FAILED"

            print("Result: SUCCESS")
            print("Test Case FAILED")


    
    
    

    with open(report_file, "a") as report:

        report.write(f"Test Case {index}\n")
        report.write(f"Username: {username}\n")
        report.write(f"Expected Result: {expected_result}\n")
        report.write(f"Actual Result: {actual_result}\n")
        report.write(f"Status: {test_status}\n")
        report.write("-------------------------------------\n")


    
    
    

    driver.quit()


print("--------------------------------")
print("Assignment 8 execution completed")
print("Report generated successfully.")
print("Report:", report_file)