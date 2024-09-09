import streamlit as st
import csv
import pyodbc
import psycopg2  # Importing psycopg2 for PostgreSQL connection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Streamlit UI
st.title("Airport Data Extraction and Database Insertion")
st.sidebar.title("Settings")

def extract_data_for_country_and_type(country_name, airport_type):
    # Set up Chrome options (optional, e.g., to run headlessly)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment to run in headless mode if GUI is not needed

    st.write("Setting up ChromeDriver with webdriver-manager...")
    # Automatically manage the ChromeDriver installation and setup using webdriver-manager
    service = Service(ChromeDriverManager().install())

    # Set up the WebDriver with the managed service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    st.write("ChromeDriver setup complete.")

    # SQL Server connection details (commented out)
    # sql_server_config = {
    #     'server': '185.4.176.50,5672',
    #     'database': '',
    #     'username': '',
    #     'password': ''
    # }

    # PostgreSQL connection details
    postgres_config = {
        'host': 'localhost',
        'database': 'IATASave',
        'user': 'postgres',
        'password': '5588',
        'port': '5432'  # Default port for PostgreSQL
    }

    try:
        # Connect to SQL Server database (commented out)
        # st.write("Connecting to the SQL Server database...")
        # sql_server_connection = pyodbc.connect(
        #     'DRIVER={ODBC Driver 17 for SQL Server};'
        #     f'SERVER={sql_server_config["server"]};'
        #     f'DATABASE={sql_server_config["database"]};'
        #     f'UID={sql_server_config["username"]};'
        #     f'PWD={sql_server_config["password"]}'
        # )
        # sql_server_cursor = sql_server_connection.cursor()
        # st.success("Connected to SQL Server successfully.")

        # Connect to PostgreSQL database
        st.write("Connecting to the PostgreSQL database...")
        postgres_connection = psycopg2.connect(
            host=postgres_config['host'],
            database=postgres_config['database'],
            user=postgres_config['user'],
            password=postgres_config['password'],
            port=postgres_config['port']
        )
        postgres_cursor = postgres_connection.cursor()
        st.success("Connected to PostgreSQL successfully.")

        # Access the specific page
        st.write("Navigating to the target webpage...")
        driver.get("https://airportcodes.io/en/all-airports/")
        st.write("Page loaded. Waiting for elements to fully load...")
        time.sleep(5)  # Wait for the page to load completely

        # Ensure the dropdown is loaded and visible using JavaScript
        st.write("Ensuring the Country dropdown is visible and interactable...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "country"))
        )
        dropdown_country = driver.find_element(By.NAME, "country")
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_country)
        driver.execute_script("arguments[0].style.visibility='visible'; arguments[0].style.display='block';", dropdown_country)
        st.write("Country dropdown visibility ensured.")

        # Initialize the Select class for Country
        st.write("Initializing Select class for the Country dropdown...")
        select_country = Select(dropdown_country)
        st.write("Country dropdown initialized.")

        # Select the country based on user input
        try:
            st.write(f"Selecting '{country_name}' from the Country dropdown...")
            select_country.select_by_visible_text(country_name)
            st.write(f"'{country_name}' selected.")
        except Exception as e:
            st.error(f"Error selecting '{country_name}': {e}")
            return  # Exit the function if an error occurs

        # Ensure the airport type dropdown is loaded and visible if specified
        if airport_type.lower() != "any":
            st.write("Ensuring the Airport Type dropdown is visible and interactable...")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "type"))
            )
            dropdown_type = driver.find_element(By.NAME, "type")
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_type)
            driver.execute_script("arguments[0].style.visibility='visible'; arguments[0].style.display='block';", dropdown_type)
            st.write("Airport Type dropdown visibility ensured.")

            # Initialize the Select class for Airport Type
            st.write("Initializing Select class for the Airport Type dropdown...")
            select_type = Select(dropdown_type)
            st.write("Airport Type dropdown initialized.")

            # Select the airport type based on user input
            try:
                st.write(f"Selecting '{airport_type}' from the Airport Type dropdown...")
                select_type.select_by_visible_text(airport_type)
                st.write(f"'{airport_type}' selected.")
            except Exception as e:
                st.error(f"Error selecting '{airport_type}': {e}")
                return  # Exit the function if an error occurs

        # Wait for 5 seconds to ensure data starts loading
        st.write("Waiting for 5 seconds before starting data extraction...")
        time.sleep(5)

        def fetch_elements():
            """Fetch the latest elements for IATA, Name, City, and Country."""
            return {
                "iata": driver.find_elements(By.XPATH, "//tr/td[2]"),
                "name": driver.find_elements(By.XPATH, "//tr/td[3]"),
                "city": driver.find_elements(By.CSS_SELECTOR, "tbody tr td:nth-child(5)"),
                "country": driver.find_elements(By.XPATH, "//tbody/tr/td[6]")
            }

        st.write("Extracting data from the first page...")
        elements = fetch_elements()
        st.write(f"First page: Found {len(elements['iata'])} IATA rows.")

        # Click the "Load more" button using CSS selector until all data with IATA codes are loaded
        page_count = 1
        while True:
            try:
                # Click the "Load more" button if it exists using CSS selector
                load_more_button = driver.find_element(By.CSS_SELECTOR, "button.supertable__load_more")
                
                # Scroll into view and use JavaScript click to avoid interception
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                driver.execute_script("arguments[0].click();", load_more_button)

                page_count += 1
                st.write(f"Loading data from page {page_count}...")
                time.sleep(3)  # Wait for data to load

                # Check new data loaded after clicking "Load more"
                elements = fetch_elements()
                st.write(f"Page {page_count}: Found {len(elements['iata'])} IATA rows.")
                
            except ElementClickInterceptedException:
                st.warning("Element click intercepted, attempting JavaScript click...")
                try:
                    driver.execute_script("arguments[0].click();", load_more_button)
                except Exception as e:
                    st.error(f"Failed to click 'Load more' using JavaScript: {e}")
                    break

            except NoSuchElementException:
                st.write("No more 'Load more' button found or unable to click. Proceeding with extraction...")
                break

            # Check if the count of visible rows matches the loaded count
            try:
                visible_count_element = driver.find_element(By.XPATH, "//span[@class='supertable__count_visible']")
                visible_count = int(visible_count_element.text)
                st.write(f"Visible rows count: {visible_count}")
                
                if visible_count == 0:
                    st.write("All rows loaded. Proceeding with data extraction...")
                    break
            except Exception as e:
                st.error(f"Error retrieving visible count: {e}")
                break

        # Validate that all necessary columns have data
        iata_values = elements['iata']
        name_values = elements['name']
        city_values = elements['city']
        country_values = elements['country']

        # Use the minimum length to avoid IndexError
        min_length = min(len(iata_values), len(name_values), len(city_values), len(country_values))
        st.write(f"Proceeding with {min_length} rows for extraction.")

        data = []
        for i in range(min_length):
            try:
                iata = iata_values[i].text.strip()  # Remove extra spaces
                name = name_values[i].text.strip()  # Remove extra spaces
                city = city_values[i].text.strip()  # Remove extra spaces
                country = country_values[i].text.strip()  # Remove extra spaces

                # Only add non-empty values
                if iata and name and city and country:
                    st.write(f"Row {i+1}: IATA: {iata}, Name: {name}, City: {city}, Country: {country}")
                    data.append([iata, name, city, country])

                    # Insert the data into PostgreSQL
                    postgres_cursor.execute("""
                        INSERT INTO iatacode 
                        (aircode, airport_name, country, city_name)
                        VALUES (%s, %s, %s, %s)
                    """, (iata, name, country, city))
            except StaleElementReferenceException:
                st.warning(f"Stale element at index {i}, refetching elements...")
                elements = fetch_elements()  # Refetch the elements
                # Retry fetching data
                iata = elements['iata'][i].text.strip()
                name = elements['name'][i].text.strip()
                city = elements['city'][i].text.strip()
                country = elements['country'][i].text.strip()
                if iata and name and city and country:
                    st.write(f"Row {i+1} after refetch: IATA: {iata}, Name: {name}, City: {city}, Country: {country}")
                    data.append([iata, name, city, country])
                    postgres_cursor.execute("""
                        INSERT INTO iatacode 
                        (aircode, airport_name, country, city_name)
                        VALUES (%s, %s, %s, %s)
                    """, (iata, name, country, city))

        postgres_connection.commit()
        st.success("Data inserted into PostgreSQL database successfully.")

        # Save the extracted data to a CSV file
        csv_file = "iata_name_city_country_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["IATA", "Name", "City", "Country"])  # Header
            writer.writerows(data)

        st.success(f"IATA, Name, City, and Country data saved to {csv_file}")
        st.write(f"Total rows extracted: {len(data)}")

    finally:
        # Close the browser and database connections
        st.write("Closing the browser and database connections...")
        driver.quit()
        # sql_server_connection.close()  # Commenting out the SQL Server connection close
        postgres_connection.close()
        st.write("Browser and database connections closed.")

# Loop to handle multiple country extractions
country_count = 1
while True:
    country_name = st.sidebar.text_input(f"Enter country name {country_count}:", value="Bangladesh", key=f"country_{country_count}")
    airport_type = st.sidebar.text_input(f"Enter airport type for country {country_count}:", value="Any", key=f"type_{country_count}")
    if st.sidebar.button(f"Extract Data for {country_name} with {airport_type}", key=f"extract_{country_count}"):
        extract_data_for_country_and_type(country_name, airport_type)
    if not st.sidebar.checkbox("Add another country?", value=True, key=f"add_{country_count}"):
        break
    country_count += 1
