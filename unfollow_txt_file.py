import os
import argparse
from settings import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

BASE_URL = "https://www.instagram.com"

parser = argparse.ArgumentParser(
    description='Run the browser in headless mode or not.')
parser.add_argument('--headless', action='store_true',
                    help='Run the browser in headless mode')
args = parser.parse_args()

chrome_options = Options()
# Set headless mode based on command line argument
if args.headless:
    chrome_options.add_argument("--headless")
# Bypass OS security model, REQUIRED on Linux if running as root
chrome_options.add_argument("--no-sandbox")
# Overcome limited resource problems
chrome_options.add_argument("--disable-dev-shm-usage")
# Launches Chrome in incognito mode
chrome_options.add_argument("--incognito")

BROWSER = webdriver.Chrome(options=chrome_options)

BASE_DIR = os.getcwd()
FILE = USERNAMES_FILENAME + ".txt"
FILE_LOCATION = os.path.join(BASE_DIR, FILE)

def wait_and_click_button(button_text, user):
    try:
        # Wait for the button to be clickable. Adjust the timeout as needed.
        button = WebDriverWait(BROWSER, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(text(), '{button_text}')]|//span[contains(text(), '{button_text}')]"))
        )
        button.click()
    except WebDriverException as e:
        print(f"An error occurred with {user}: {e}")
        # Log error to file
        with open("errors.txt", "a+") as f:
            f.write(f"{user}\n")

def main():
    try:
        # Read file
        with open(FILE_LOCATION, "r") as file:
            usernames = [username.rstrip() for username in file.readlines()]
            
        # Login
        BROWSER.get(f"{BASE_URL}/accounts/login")
        username_input = WebDriverWait(BROWSER, 10).until(
            EC.element_to_be_clickable((By.NAME, 'username'))
        )
        username_input.send_keys(USERNAME)
        password_input = WebDriverWait(BROWSER, 10).until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        )
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.ENTER)
        print(f"Logged in as {USERNAME}.")
        
        # Logged in #

        # Unfollow usernames
        for user in usernames:
            print(f"Unfollowing {user}")
            BROWSER.get(f"{BASE_URL}/{user}/")
            
            # Click "Following"
            wait_and_click_button("Following", user)
            # Click "Unfollow"
            wait_and_click_button("Unfollow", user)
            
            print("-" * 50)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # This block ensures that the browser is closed even if an error occurs.
        BROWSER.quit()

if __name__ == "__main__":
    main()