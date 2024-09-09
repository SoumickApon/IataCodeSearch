import streamlit as st
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

# Streamlit UI
st.title("Airport Data Extraction and Database Insertion")
st.sidebar.title("Settings")

# Sidebar inputs
country_name = st.sidebar.text_input("Enter the country name:", "Bangladesh")
if st.sidebar.button("Start Extraction"):
    # Set up Chrome options (optional, e.g., to run headlessly)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment to run in headless mode if GUI is not needed

    st.write("Setting up ChromeDriver with webdriver-manager...")
    # Automatically manage the ChromeDriver installation and setup using webdriver-manager
    service = Service(ChromeDriverManager().install())

    # Set up the WebDriver with the managed service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    st.write("ChromeDriver setup complete.")

    # Database connection details
    db_config = {
        'server': '',
        'database': '',
        'username': '',
        'password': ''
    }

    try:
        # Connect to the SQL Server database
        st.write("Connecting to the SQL Server database...")
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={db_config["server"]};'
            f'DATABASE={db_config["database"]};'
            f'UID={db_config["username"]};'
            f'PWD={db_config["password"]}'
        )
        cursor = connection.cursor()
        st.success("Database connected successfully.")

        # Access the specific page
        st.write("Navigating to the target webpage...")
        driver.get("https://airportcodes.io/en/all-airports/")
        st.write("Page loaded. Waiting for elements to fully load...")
        time.sleep(5)  # Wait for the page to load completely

        # Ensure the dropdown is loaded and visible using JavaScript
        st.write("Using JavaScript to ensure the dropdown is visible and interactable...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "country"))
        )
        dropdown = driver.find_element(By.NAME, "country")

        # Scroll into view and make sure the dropdown is interactable using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        driver.execute_script("arguments[0].style.visibility='visible'; arguments[0].style.display='block';", dropdown)
        st.write("Dropdown visibility ensured with JavaScript.")

        # Initialize the Select class with the dropdown element
        st.write("Initializing Select class for the dropdown...")
        select = Select(dropdown)
        st.write("Select class initialized.")

        # Wait for 2 seconds before selecting an option
        st.write("Waiting for 2 seconds before selecting an option...")
        time.sleep(2)

        # Select the country based on user input
        try:
            st.write(f"Selecting '{country_name}' from the dropdown...")
            select.select_by_visible_text(country_name)
            st.write(f"'{country_name}' selected.")
        except Exception as e:
            st.error(f"Error selecting '{country_name}': {e}")
            raise

        # Wait for 5 seconds to ensure data starts loading
        st.write("Waiting for 5 seconds before starting data extraction...")
        time.sleep(5)

        # Locate the IATA column header to confirm it's found
        st.write("Locating the IATA column header...")
        iata_header = driver.find_element(By.XPATH, "//th[@data-column='airport.iata']")
        st.write("IATA column header found.")

        # Locate the Name column header to confirm it's found
        st.write("Locating the Name column header...")
        name_header = driver.find_element(By.XPATH, "//th[@data-column='airport.link_name']")
        st.write("Name column header found.")

        # Locate the City column header to confirm it's found
        st.write("Locating the City column header...")
        city_header = driver.find_element(By.XPATH, "//th[@data-column='city.name']")
        st.write("City column header found.")

        # Locate the Country column header to confirm it's found
        st.write("Locating the Country column header...")
        country_header = driver.find_element(By.XPATH, "//th[@data-column='country.name']")
        st.write("Country column header found.")

        # Scroll through the table to load all rows
        st.write("Scrolling through the table to load all rows...")
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
        st.write("Extracting IATA values under the IATA column...")
        iata_values = driver.find_elements(By.XPATH, "//tr/td[2]")  # Assuming IATA is the second column

        if not iata_values:
            st.write("No IATA values found using the initial XPath. Trying alternative approaches...")
            iata_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.iata')]")

        # Extract Name values from the associated column
        st.write("Extracting Name values under the Name column...")
        name_values = driver.find_elements(By.XPATH, "//tr/td[3]")  # Assuming Name is the third column

        if not name_values:
            st.write("No Name values found using the initial XPath. Trying alternative approaches...")
            name_values = driver.find_elements(By.XPATH, "//tr/td[contains(@data-column, 'airport.link_name')]")

        # Extract City values using the CSS selector for the fifth column
        st.write("Extracting City values under the City column...")
        city_values = driver.find_elements(By.CSS_SELECTOR, "tbody tr td:nth-child(5)")

        if not city_values:
            st.write("No City values found using the CSS selector. Please check the table structure.")

        # Extract Country values using the XPath for the sixth column
        st.write("Extracting Country values under the Country column...")
        country_values = driver.find_elements(By.XPATH, "//tbody/tr/td[6]")

        if not country_values:
            st.write("No Country values found using the XPath. Please check the table structure.")

        # Ensure all columns have been found and extracted
        if iata_values and name_values and city_values and country_values:
            st.write(f"Found {len(iata_values)} IATA rows, {len(name_values)} Name rows, {len(city_values)} City rows, and {len(country_values)} Country rows.")
            data = []
            for i in range(len(iata_values)):
                iata = iata_values[i].text.strip()  # Remove extra spaces
                name = name_values[i].text.strip()  # Remove extra spaces
                city = city_values[i].text.strip()  # Remove extra spaces
                country = country_values[i].text.strip()  # Remove extra spaces

                # Only add non-empty values
                if iata and name and city and country:
                    st.write(f"Row {i+1}: IATA: {iata}, Name: {name}, City: {city}, Country: {country}")
                    data.append([iata, name, city, country])

                    # Insert the data into the database
                    cursor.execute("""
                        INSERT INTO [Samriddhi_DB].[dbo].[IATACode] 
                        ([AirCode], [Airport_Name], [Country], [City_Name])
                        VALUES (?, ?, ?, ?)
                    """, (iata, name, country, city))
            connection.commit()
            st.success("Data inserted into the database successfully.")

            # Save the extracted data to a CSV file
            csv_file = "iata_name_city_country_data.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["IATA", "Name", "City", "Country"])  # Header
                writer.writerows(data)

            st.success(f"IATA, Name, City, and Country data saved to {csv_file}")
            st.write(f"Total rows extracted: {len(data)}")
        else:
            st.error("Unable to extract all columns (IATA, Name, City, Country). Please check the table structure.")

    finally:
        # Close the browser and database connection
        st.write("Closing the browser and database connection...")
        driver.quit()
        connection.close()
        st.write("Browser and database connection closed.")
