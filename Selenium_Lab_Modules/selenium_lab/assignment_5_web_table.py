from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://the-internet.herokuapp.com/tables")
table = driver.find_element(By.ID, "table1")
rows = table.find_elements(By.TAG_NAME, "tr")
print("Total rows:", len(rows))
for row in rows:

    columns = row.find_elements(By.TAG_NAME, "td")

    if columns:

        print("--------------------------------")

        for column in columns:
            print(column.text)
target_name = "Doe"

person_found = False

for row in rows:

    columns = row.find_elements(By.TAG_NAME, "td")

    if columns:

        last_name = columns[0].text
        first_name = columns[1].text

        if last_name == target_name:

            email = columns[2].text
            due = columns[3].text
            website = columns[4].text

            print("--------------------------------")
            print("Person found:", first_name, last_name)
            print("Email:", email)
            print("Due:", due)
            print("Website:", website)

            person_found = True
            break
assert person_found, f"Person with last name '{target_name}' was not found."
print("--------------------------------")
print("Assignment 5 PASSED")
with open("reports/assignment_5_report.txt", "w") as file:
    file.write("Assignment 5 - HTML Web Table Extractor\n")
    file.write("Status: PASSED\n")
    file.write("Person: Jason Doe\n")
    file.write("Email: jdoe@hotmail.com\n")
    file.write("Due: $100.00\n")
    file.write("Website: http://www.jdoe.com\n")

print("Report generated successfully.")

driver.quit()
driver.quit()