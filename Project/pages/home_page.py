# Home page object is to handle the note related functionality

from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure

class HomePage(BasePage):
    #Locators
    HOME_LINK = (By.CSS_SELECTOR, "a[data-testid='home']")
    
    def __init__(self, driver):
        """Initialize HomePage with WebDriver instance."""
        super().__init__(driver)
        
    def is_home_page_loaded(self):
        """Check if home page is loaded successfully."""
        try:
            # Wait for any of the home page indicators to be visible
            if self.is_element_visible(self.HOME_LINK, timeout=10):
                self.logger.info("Home page is loaded successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking home page load: {e}")
            return False
        
    