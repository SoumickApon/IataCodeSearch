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

#     # Locate the IATA column header to confirm it's found
#     print("Locating the IATA column header...")
#     iata_header = driver.find_element(By.XPATH, "//th[@data-column='airport.iata']")
#     print("IATA column header found.")

#     # Scroll through the table to load all rows
#     print("Scrolling through the table to load all rows...")
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     scroll_attempts = 0
#     max_scroll_attempts = 10  # Limit the number of scroll attempts

#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Adjust time if loading takes longer
#         new_height = driver.execute_script("return document.body.scrollHeight")
        
#         # Break if no more new content is loaded or if the max attempts are reached
#         if new_height == last_height or scroll_attempts >= max_scroll_attempts:
#             break
#         last_height = new_height
#         scroll_attempts += 1

#     # Try different ways to find the correct XPath for IATA values
#     print("Attempting to extract IATA values...")
#     iata_values = driver.find_elements(By.XPATH, "//tr/td[2]")  # Assuming IATA is the second column

#     if not iata_values:
#         print("No IATA values found using the initial XPath. Trying alternative approaches...")
#         # Try another way if the first approach fails
#         iata_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.iata')]")

#     if iata_values:
#         print(f"Found {len(iata_values)} IATA rows.")
#         data = []
#         for i, iata in enumerate(iata_values, start=1):
#             print(f"Row {i}: IATA: {iata.text}")
#             data.append([iata.text])

#         # Save the extracted data to a CSV file
#         csv_file = "iata_data.csv"
#         with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(["IATA"])  # Header
#             writer.writerows(data)

#         print(f"IATA data saved to {csv_file}")
#         print(f"Total IATA rows extracted: {len(data)}")
#     else:
#         print("Still no IATA values found. Please review the table structure or XPath.")

# finally:
#     # Close the browser
#     print("Closing the browser...")
#     driver.quit()
#     print("Browser closed.")
#========================================================

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

#     # Locate the IATA column header to confirm it's found
#     print("Locating the IATA column header...")
#     iata_header = driver.find_element(By.XPATH, "//th[@data-column='airport.iata']")
#     print("IATA column header found.")

#     # Locate the Name column header to confirm it's found
#     print("Locating the Name column header...")
#     name_header = driver.find_element(By.XPATH, "//th[@data-column='airport.link_name']")
#     print("Name column header found.")

#     # Scroll through the table to load all rows
#     print("Scrolling through the table to load all rows...")
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     scroll_attempts = 0
#     max_scroll_attempts = 10  # Limit the number of scroll attempts

#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Adjust time if loading takes longer
#         new_height = driver.execute_script("return document.body.scrollHeight")
        
#         # Break if no more new content is loaded or if the max attempts are reached
#         if new_height == last_height or scroll_attempts >= max_scroll_attempts:
#             break
#         last_height = new_height
#         scroll_attempts += 1

#     # Extract IATA values from the associated column
#     print("Extracting IATA values under the IATA column...")
#     iata_values = driver.find_elements(By.XPATH, "//tr/td[2]")  # Assuming IATA is the second column

#     if not iata_values:
#         print("No IATA values found using the initial XPath. Trying alternative approaches...")
#         iata_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.iata')]")

#     # Extract Name values from the associated column
#     print("Extracting Name values under the Name column...")
#     name_values = driver.find_elements(By.XPATH, "//tr/td[3]")  # Assuming Name is the third column

#     if not name_values:
#         print("No Name values found using the initial XPath. Trying alternative approaches...")
#         name_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.link_name')]")

#     # Ensure both columns have been found and extracted
#     if iata_values and name_values:
#         print(f"Found {len(iata_values)} IATA rows and {len(name_values)} Name rows.")
#         data = []
#         for i in range(len(iata_values)):
#             iata = iata_values[i].text
#             name = name_values[i].text
#             print(f"Row {i+1}: IATA: {iata}, Name: {name}")
#             data.append([iata, name])

#         # Save the extracted data to a CSV file
#         csv_file = "iata_name_data.csv"
#         with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(["IATA", "Name"])  # Header
#             writer.writerows(data)

#         print(f"IATA and Name data saved to {csv_file}")
#         print(f"Total rows extracted: {len(data)}")
#     else:
#         print("Unable to extract both IATA and Name values. Please check the table structure.")

# finally:
#     # Close the browser
#     print("Closing the browser...")
#     driver.quit()
#     print("Browser closed.")

#=========================================

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

    # Locate the IATA column header to confirm it's found
    print("Locating the IATA column header...")
    iata_header = driver.find_element(By.XPATH, "//th[@data-column='airport.iata']")
    print("IATA column header found.")

    # Locate the Name column header to confirm it's found
    print("Locating the Name column header...")
    name_header = driver.find_element(By.XPATH, "//th[@data-column='airport.link_name']")
    print("Name column header found.")

    # Locate the City column header to confirm it's found
    print("Locating the City column header...")
    city_header = driver.find_element(By.XPATH, "//th[@data-column='city.name']")
    print("City column header found.")

    # Scroll through the table to load all rows
    print("Scrolling through the table to load all rows...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    max_scroll_attempts = 10  # Limit the number of scroll attempts

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust time if loading takes longer
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break if no more new content is loaded or if the max attempts are reached
        if new_height == last_height or scroll_attempts >= max_scroll_attempts:
            break
        last_height = new_height
        scroll_attempts += 1

    # Extract IATA values from the associated column
    print("Extracting IATA values under the IATA column...")
    iata_values = driver.find_elements(By.XPATH, "//tr/td[2]")  # Assuming IATA is the second column

    if not iata_values:
        print("No IATA values found using the initial XPath. Trying alternative approaches...")
        iata_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.iata')]")

    # Extract Name values from the associated column
    print("Extracting Name values under the Name column...")
    name_values = driver.find_elements(By.XPATH, "//tr/td[3]")  # Assuming Name is the third column

    if not name_values:
        print("No Name values found using the initial XPath. Trying alternative approaches...")
        name_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.link_name')]")

    # Extract City values from the associated column
    print("Extracting City values under the City column...")
    city_values = driver.find_elements(By.XPATH, "//tr/td[4]")  # Assuming City is the fourth column

    if not city_values:
        print("No City values found using the initial XPath. Trying alternative approaches...")
        city_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'city.name')]")

    # Ensure all columns have been found and extracted
    if iata_values and name_values and city_values:
        print(f"Found {len(iata_values)} IATA rows, {len(name_values)} Name rows, and {len(city_values)} City rows.")
        data = []
        for i in range(len(iata_values)):
            iata = iata_values[i].text.strip()  # Remove extra spaces
            name = name_values[i].text.strip()  # Remove extra spaces
            city = city_values[i].text.strip()  # Remove extra spaces

            # Only add non-empty values
            if iata and name and city:
                print(f"Row {i+1}: IATA: {iata}, Name: {name}, City: {city}")
                data.append([iata, name, city])

        # Save the extracted data to a CSV file
        csv_file = "iata_name_city_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["IATA", "Name", "City"])  # Header
            writer.writerows(data)

        print(f"IATA, Name, and City data saved to {csv_file}")
        print(f"Total rows extracted: {len(data)}")
    else:
        print("Unable to extract all columns (IATA, Name, City). Please check the table structure.")

finally:
    # Close the browser
    print("Closing the browser...")
    driver.quit()
    print("Browser closed.")
