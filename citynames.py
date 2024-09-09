# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # Set up Chrome options (optional, e.g., to run headlessly)
# chrome_options = Options()
# # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode if GUI is not needed

# print("Setting up ChromeDriver with webdriver-manager...")
# # Automatically manage the ChromeDriver installation and setup using webdriver-manager
# service = Service(ChromeDriverManager().install())

# # Set up the WebDriver with the managed service
# driver = webdriver.Chrome(service=service, options=chrome_options)
# print("ChromeDriver setup complete.")

# try:
#     # Access the specific page
#     print("Navigating to the target webpage...")
#     driver.get("https://airportcodes.io/en/all-airports/")
#     print("Page loaded. Waiting for elements to fully load...")
#     time.sleep(5)  # Wait for the page to load completely

#     # Ensure the dropdown is loaded and visible using JavaScript
#     print("Using JavaScript to ensure the dropdown is visible and interactable...")
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.NAME, "country"))
#     )
#     dropdown = driver.find_element(By.NAME, "country")

#     # Scroll into view and make sure the dropdown is interactable using JavaScript
#     driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
#     driver.execute_script("arguments[0].style.visibility='visible'; arguments[0].style.display='block';", dropdown)
#     print("Dropdown visibility ensured with JavaScript.")

#     # Initialize the Select class with the dropdown element
#     print("Initializing Select class for the dropdown...")
#     select = Select(dropdown)
#     print("Select class initialized.")

#     # Wait for 2 seconds before selecting an option
#     print("Waiting for 2 seconds before selecting an option...")
#     time.sleep(2)

#     # Select the "Bangladesh" option by visible text
#     print("Selecting 'Bangladesh' from the dropdown...")
#     select.select_by_visible_text("Bangladesh")
#     print("'Bangladesh' selected.")

#     # Wait for 5 seconds to ensure data starts loading
#     print("Waiting for 5 seconds before starting data extraction...")
#     time.sleep(5)

#     # Try to locate and extract city names using their text values
#     try:
#         print("Attempting to locate City values using text matching...")
#         # Example cities for XPath matching, can be adjusted or extended as needed
#         city_names = ["Barisal", "Dhaka", "Chittagong"]  # Replace with actual city names to match
#         city_values = []

#         for city in city_names:
#             # Find each city using its text
#             city_elements = driver.find_elements(By.XPATH, f"//td[normalize-space()='{city}']")
#             if city_elements:
#                 print(f"Found {len(city_elements)} rows for city: {city}")
#                 for i, element in enumerate(city_elements, start=1):
#                     city_text = element.text.strip()
#                     print(f"Row {i}: City: {city_text}")
#                     city_values.append(city_text)
#             else:
#                 print(f"No data found for city: {city}")

#         if city_values:
#             print(f"Total city values extracted: {len(city_values)}")
#         else:
#             print("No city values extracted. Please check the table structure.")

#     except Exception as e:
#         print(f"Unable to extract City data. Error: {e}")

# finally:
#     # Close the browser
#     print("Closing the browser...")
#     driver.quit()
#     print("Browser closed.")


#====================================================

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options (optional, e.g., to run headlessly)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode if GUI is not needed

print("Setting up ChromeDriver with webdriver-manager...")
# Automatically manage the ChromeDriver installation and setup using webdriver-manager
service = Service(ChromeDriverManager().install())

# Set up the WebDriver with the managed service
driver = webdriver.Chrome(service=service, options=chrome_options)
print("ChromeDriver setup complete.")

try:
    # Access the specific page
    print("Navigating to the target webpage...")
    driver.get("https://airportcodes.io/en/all-airports/")
    print("Page loaded. Waiting for elements to fully load...")
    time.sleep(5)  # Wait for the page to load completely

    # Ensure the dropdown is loaded and visible using JavaScript
    print("Using JavaScript to ensure the dropdown is visible and interactable...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "country"))
    )
    dropdown = driver.find_element(By.NAME, "country")

    # Scroll into view and make sure the dropdown is interactable using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    driver.execute_script("arguments[0].style.visibility='visible'; arguments[0].style.display='block';", dropdown)
    print("Dropdown visibility ensured with JavaScript.")

    # Initialize the Select class with the dropdown element
    print("Initializing Select class for the dropdown...")
    select = Select(dropdown)
    print("Select class initialized.")

    # Wait for 2 seconds before selecting an option
    print("Waiting for 2 seconds before selecting an option...")
    time.sleep(2)

    # Select the "Bangladesh" option by visible text
    print("Selecting 'Bangladesh' from the dropdown...")
    select.select_by_visible_text("Bangladesh")
    print("'Bangladesh' selected.")

    # Wait for 5 seconds to ensure data starts loading
    print("Waiting for 5 seconds before starting data extraction...")
    time.sleep(5)

    # Extract city names using CSS selectors
    try:
        print("Attempting to extract city names using CSS selectors...")

        # Locate city names in the fifth column of each row in the table body
        city_values = driver.find_elements(By.CSS_SELECTOR, "tbody tr td:nth-child(5)")

        if city_values:
            print(f"Found {len(city_values)} City rows.")
            for i, element in enumerate(city_values, start=1):
                city_text = element.text.strip()
                print(f"Row {i}: City: {city_text}")
        else:
            print("No city values extracted. Please check the table structure.")

    except Exception as e:
        print(f"Unable to extract City data. Error: {e}")

finally:
    # Close the browser
    print("Closing the browser...")
    driver.quit()
    print("Browser closed.")


