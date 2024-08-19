import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

# LinkedIn credentials
username_str = 'sharan.singh0203@gmail.com'
password_str = 'hitohitonomi3'

# Specify the path to the ChromeDriver using the Service class
service = Service(executable_path=r'C:\Users\epicn\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')

# Initialize the Chrome driver using the service
driver = webdriver.Chrome(service=service)

# Implicit wait
driver.implicitly_wait(5)

# Open LinkedIn login page
driver.get('https://www.linkedin.com/login')
print("Opened LinkedIn login page")

# Log in to LinkedIn
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')

username.send_keys(username_str)
password.send_keys(password_str)
password.send_keys(Keys.RETURN)
print("Logged in successfully")

# Close any open chat windows
try:
    close_chat_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Dismiss"]'))
    )
    close_chat_button.click()
    print("Closed chat window")
except:
    print("No chat window to close")

# Navigate directly to the specific LinkedIn "People" page with the search query already applied
people_page_url = 'https://www.linkedin.com/company/github/people/?keywords=Software%20Engineer'
WebDriverWait(driver, 10).until(EC.url_contains('/feed/'))  # Ensure that login completed by checking if the URL changes
driver.get(people_page_url)
print(f"Navigated to the LinkedIn people page: {people_page_url}")

# Specify how many connection requests to send
num_requests = 20
requests_sent = 0

# Keep sending connection requests until the desired number is reached
while requests_sent < num_requests:
    try:
        # Refetch the list of "Connect" buttons
        connect_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@aria-label, "Invite") and .//span[text()="Connect"]]'))
        )

        if not connect_buttons:
            print("No more connect buttons found.")
            break

        # Send connection request
        connect_buttons[0].click()
        
        # Wait for 3 seconds before clicking "Send without a note"
        time.sleep(3)

        # Handle the "Send without a note" button
        send_without_note = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button//span[text()="Send without a note"]'))
        )
        send_without_note.click()

        requests_sent += 1
        print(f"Connection request sent to person {requests_sent}")

        time.sleep(random.uniform(7, 12))  # Random delay to avoid detection and avoid getting blocked by LinkedIn

    except ElementClickInterceptedException:
        print(f"Click intercepted for person {requests_sent + 1}, retrying...")
        driver.execute_script("arguments[0].click();", connect_buttons[0])
    except Exception as e:
        print(f"Error sending request to person {requests_sent + 1}: {e}")
        break

# Close the browser
driver.quit()
print("Closed the browser")
