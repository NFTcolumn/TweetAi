from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Twitter login page
    driver.get('https://twitter.com/i/flow/login')

    # Wait for the username field to be visible
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    
    # Enter username and click next
    username_field.send_keys('nftmansa')
    username_field.send_keys(Keys.RETURN)
    
    # Wait for password field and enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys('c4n74ack7thisFipr42Lance0x7$')
    password_field.send_keys(Keys.RETURN)

    # Wait for the home page to load
    time.sleep(5)

    # Save the cookies for later use
    cookies = driver.get_cookies()
    
    # Save cookies to a file
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)
        
    print("Login successful and cookies saved!")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()
