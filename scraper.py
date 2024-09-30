from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome WebDriver with options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (browser won't open)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def search_flights(origin, destination, depart_date, return_date=None, passengers=1, flight_class='economy'):
    try:
        # Open Google Flights
        driver.get("https://www.google.com/flights")

        # Wait for page to load
        time.sleep(2)

        # Find and input origin
        origin_input = driver.find_element(By.XPATH, "//input[@placeholder='Where from?']")
        origin_input.clear()
        origin_input.send_keys(origin)
        time.sleep(1)
        origin_input.send_keys(Keys.ENTER)

        # Find and input destination
        dest_input = driver.find_element(By.XPATH, "//input[@placeholder='Where to?']")
        dest_input.clear()
        dest_input.send_keys(destination)
        time.sleep(1)
        dest_input.send_keys(Keys.ENTER)

        # Select departure date
        date_input = driver.find_element(By.XPATH, "//input[@aria-label='Departure date']")
        date_input.click()
        time.sleep(1)

        # Set the desired departure date
        depart_button = driver.find_element(By.XPATH, f"//div[@aria-label='{depart_date}']")
        depart_button.click()

        # If return_date is provided, select it
        if return_date:
            return_button = driver.find_element(By.XPATH, f"//div[@aria-label='{return_date}']")
            return_button.click()

        # Click Done
        done_button = driver.find_element(By.XPATH, "//button[text()='Done']")
        done_button.click()

        # Specify passengers and class
        passengers_input = driver.find_element(By.XPATH, "//button[@aria-label='Number of passengers']")
        passengers_input.click()
        time.sleep(1)

        # Adjust number of passengers
        for _ in range(passengers - 1):
            add_passenger_button = driver.find_element(By.XPATH, "//button[@aria-label='Increase number of adults']")
            add_passenger_button.click()

        # Select flight class
        flight_class_dropdown = driver.find_element(By.XPATH, "//div[text()='Economy']")
        flight_class_dropdown.click()
        time.sleep(1)
        flight_class_option = driver.find_element(By.XPATH, f"//div[text()='{flight_class.capitalize()}']")
        flight_class_option.click()

        # Click done to confirm passenger and class selection
        confirm_passenger_class_button = driver.find_element(By.XPATH, "//button[text()='Done']")
        confirm_passenger_class_button.click()

        # Submit the search
        search_button = driver.find_element(By.XPATH, "//button[@aria-label='Search']")
        search_button.click()

        # Wait for the results to load
        time.sleep(5)

        # Scrape flight details: prices, airlines, duration
        flight_prices = driver.find_elements(By.XPATH, "//div[@class='gws-flights-results__price']")
        flight_airlines = driver.find_elements(By.XPATH, "//span[@class='gws-flights__ellipsize gws-flights__ellipsize__dinner']")
        flight_durations = driver.find_elements(By.XPATH, "//div[@class='gws-flights-results__duration']")

        # Print the first 10 flights
        for i in range(min(10, len(flight_prices))):
            price = flight_prices[i].text
            airline = flight_airlines[i].text if i < len(flight_airlines) else "Unknown Airline"
            duration = flight_durations[i].text if i < len(flight_durations) else "Unknown Duration"
            print(f"Flight {i + 1}: Price: {price}, Airline: {airline}, Duration: {duration}")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

# Example usage with more features
search_flights(
    origin="",
    destination="",
    depart_date="",
    return_date="",
    passengers=,
    flight_class=""
)
