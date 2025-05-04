from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import docker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRunner:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        firefox_options = Options()
        firefox_options.add_argument('--start-maximized')
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("dom.push.enabled", False)
        firefox_options.set_preference("signon.rememberSignons", False)
        firefox_options.set_preference("signon.autofillForms", False)
        firefox_options.set_preference("signon.management.page.enabled", False)
        self.driver = webdriver.Firefox(options=firefox_options)
        logger.info("Browser started")

    def test_localhost(self):
        try:
            self.driver.get("http://localhost/")
            logger.info("Accessing localhost...")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Localhost test failed: {str(e)}")
            raise

    def test_login(self):
        try:
            self.driver.get("http://localhost/users/login/")
            logger.info("Accessing login page...")
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys("student")
            password_field.send_keys("password")
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            logger.info("Login completed")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Login test failed: {str(e)}")
            raise

    def test_enroll(self):
        try:
            enroll_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "blue_button"))
            )
            logger.info("Found enroll button")
            
            enroll_button.click()
            logger.info("Clicked enroll button")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Enroll test failed: {str(e)}")
            raise

    def test_enter_course(self):
        try:
            course_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "green_button"))
            )
            logger.info("Found 'Přejít do kurzu' button")
            
            course_button.click()
            logger.info("Clicked 'Přejít do kurzu' button")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Enter course test failed: {str(e)}")
            raise

    def test_go_to_project(self):
        try:
            project_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.inline-flex.items-center.px-4.py-2.bg-blue-600"))
            )
            logger.info("Found 'Přejít k projektu' button")
            
            project_button.click()
            logger.info("Clicked 'Přejít k projektu' button")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Go to project test failed: {str(e)}")
            raise

    def test_open_menu(self):
        try:
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-drawer-target='drawer-navigation']"))
            )
            logger.info("Found menu button")
            menu_button.click()
            logger.info("Clicked menu button")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Open menu test failed: {str(e)}")
            raise

    def test_click_content(self):
        try:
            content_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.flex-1.ms-3.whitespace-nowrap"))
            )
            logger.info("Found 'Projekty a učební obsah' link")
            content_link.click()
            logger.info("Clicked 'Projekty a učební obsah' link")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Click content test failed: {str(e)}")
            raise

    def test_complete_and_next(self):
        try:
            complete_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.blue_button[onclick*='complete_and_next']"))
            )
            logger.info("Found 'Splinit a přejít na další kapitolu' button")
            complete_button.click()
            logger.info("Clicked 'Splinit a přejít na další kapitolu' button")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Complete and next test failed: {str(e)}")
            raise

    def test_access_demo_overview(self):
        try:
            self.driver.get("http://localhost/demos/overview/c-django/")
            logger.info("Accessing demo overview page...")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Access demo overview test failed: {str(e)}")
            raise

    def test_access_test_overview(self):
        try:
            self.driver.get("http://localhost/tests/overview/c-django/")
            logger.info("Accessing test overview page...")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Access test overview test failed: {str(e)}")
            raise

def restart_migrations():
    try:
        client = docker.from_env()
        container = client.containers.get('django-migrations-1')
        container.restart()
        logger.info("Successfully restarted migrations container")
    except Exception as e:
        logger.error(f"Failed to restart migrations container: {str(e)}")
        raise

if __name__ == "__main__":
    restart_migrations()
    time.sleep(10)  # Wait for migrations to complete
    
    runner = TestRunner()
    try:
        runner.test_localhost()
        runner.test_login()
        runner.test_enroll()
        runner.test_enter_course()
        runner.test_go_to_project()
        runner.test_open_menu()
        runner.test_click_content()
        runner.test_complete_and_next()
        runner.test_access_demo_overview()
        runner.test_access_test_overview()
        input("Press Enter to close the browser...")
    finally:
        if runner.driver:
            runner.driver.quit()