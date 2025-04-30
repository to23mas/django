from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.driver = None
        self.screenshot_dir = "selenium_screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        return self.driver

    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")

    def wait_and_find_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.take_screenshot(f"timeout_{value}")
            raise

    def safe_click(self, element, max_retries=3):
        for attempt in range(max_retries):
            try:
                # Highlight element before clicking
                self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
                time.sleep(0.5)
                element.click()
                # Remove highlight after clicking
                self.driver.execute_script("arguments[0].style.border=''", element)
                return True
            except ElementClickInterceptedException:
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)
        return False

    def login(self):
        try:
            self.driver.get(f"{self.base_url}/login/")
            
            username_field = self.wait_and_find_element(By.NAME, "username")
            password_field = self.wait_and_find_element(By.NAME, "password")
            
            # Highlight fields while typing
            self.driver.execute_script("arguments[0].style.border='3px solid green'", username_field)
            username_field.clear()
            username_field.send_keys("student")
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].style.border=''", username_field)
            
            self.driver.execute_script("arguments[0].style.border='3px solid green'", password_field)
            password_field.clear()
            password_field.send_keys("password")
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].style.border=''", password_field)
            
            login_button = self.wait_and_find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.safe_click(login_button)
            
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(f"{self.base_url}/login/")
            )
            logger.info("Successfully logged in!")
            
        except Exception as e:
            self.take_screenshot("login_failure")
            raise Exception(f"Login failed: {str(e)}")

    def navigate_and_interact(self):
        try:
            time.sleep(2)
            
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button")
            logger.info(f"Found {len(clickable_elements)} clickable elements")
            
            for element in clickable_elements[:3]:
                try:
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text or element.get_attribute("value") or "unnamed_element"
                        logger.info(f"Attempting to interact with: {element_text}")
                        
                        # Highlight element before scrolling
                        self.driver.execute_script("arguments[0].style.border='3px solid blue'", element)
                        time.sleep(0.5)
                        
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(0.5)
                        
                        self.safe_click(element)
                        time.sleep(1)
                        
                        self.take_screenshot(f"after_click_{element_text}")
                        
                        if self.driver.current_url != self.base_url:
                            self.driver.back()
                            time.sleep(1)
                            
                except Exception as e:
                    logger.warning(f"Failed to interact with element: {str(e)}")
                    continue

        except Exception as e:
            self.take_screenshot("interaction_failure")
            raise Exception(f"Navigation and interaction failed: {str(e)}")

    def run_test(self):
        try:
            self.setup_driver()
            self.login()
            self.navigate_and_interact()
            
            logger.info("Test completed successfully!")
            time.sleep(5)  # Keep browser open for 5 seconds after completion
            
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            self.take_screenshot("test_failure")
            time.sleep(5)  # Keep browser open for 5 seconds after failure
            raise
            
        finally:
            if self.driver:
                self.driver.quit()

def main():
    test = SeleniumTest()
    test.run_test()

if __name__ == "__main__":
    main() 