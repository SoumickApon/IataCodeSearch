import csv
import pyodbc
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

# Database connection details
db_config = {
    'server': '',
    'database': '',
    'username': '',
    'password': ''
}

try:
    # Connect to the SQL Server database
    print("Connecting to the SQL Server database...")
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={db_config["server"]};'
        f'DATABASE={db_config["database"]};'
        f'UID={db_config["username"]};'
        f'PWD={db_config["password"]}'
    )
    cursor = connection.cursor()
    print("Database connected successfully.")

    # Ask the user to input the country name
    country_name = input("Please enter the country name: ").strip()

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

    # Select the country based on user input
    try:
        print(f"Selecting '{country_name}' from the dropdown...")
        select.select_by_visible_text(country_name)
        print(f"'{country_name}' selected.")
    except Exception as e:
        print(f"Error selecting '{country_name}': {e}")
        raise

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

    # Extract City values using the CSS selector for the fifth column
    print("Extracting City values under the City column...")
    city_values = driver.find_elements(By.CSS_SELECTOR, "tbody tr td:nth-child(5)")

    if not city_values:
        print("No City values found using the CSS selector. Please check the table structure.")

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

                # Insert the data into the database
                cursor.execute("""
                    INSERT INTO [Samriddhi_DB].[dbo].[IATACountryCode] ([AirCode], [Airport_Name], [Country])
                    VALUES (?, ?, ?)
                """, (iata, name, city))
        connection.commit()
        print("Data inserted into the database successfully.")

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
    # Close the browser and database connection
    print("Closing the browser and database connection...")
    driver.quit()
    connection.close()
    print("Browser and database connection closed.")