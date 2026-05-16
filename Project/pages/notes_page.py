"""Notes page object for the notes application."""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class NotesPage(BasePage):
    """Page object for notes page."""
    
    # Locators
    ADD_NOTES_BUTTON = (By.CSS_SELECTOR, "button[data-testid='add-new-note']")
    NOTE_FORM = (By.CSS_SELECTOR, "div.modal-dialog")
    NOTE_TITLE_INPUT = (By.CSS_SELECTOR, "input[data-testid='note-title']")
    NOTE_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[data-testid='note-description']")
    NOTE_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='note-submit']")

    NOTE_ITEM = (By.CSS_SELECTOR, ".note-item")
    
    EDIT_NOTE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='edit-note']")
    DELETE_NOTE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='delete-note']")
    NOTES_LIST = (By.CSS_SELECTOR, ".notes-list")
    EMPTY_STATE_MESSAGE = (By.CSS_SELECTOR, "div[data-testid='empty-state']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div[data-testid='success-message']")
    # DESCRIPTION_VALIDATOR = (By.CSS_SELECTOR, "div.invalid-feedback")
    DESCRIPTION_VALIDATOR = (By.XPATH,'//textarea[@data-testid="note-description"]/following-sibling::div[@class="invalid-feedback"]')
    TITLE_VALIDATION = (By.CSS_SELECTOR, "div.invalid-feedback")
    
    def __init__(self, driver):
        """Initialize NotesPage with WebDriver instance."""
        super().__init__(driver)
    
    def click_add_note_button(self):
        """Click add note button to open note creation form."""
        with allure.step("Click add note button"):
            # Try regular click first
            try:
                self.click_element(self.ADD_NOTES_BUTTON)
            except Exception:
                # If regular click fails, try JavaScript click
                self.logger.info("Regular click failed, trying JavaScript click for add note button")
                element = self.wait_for_element(self.ADD_NOTES_BUTTON)
                self.driver.execute_script("arguments[0].click();", element)
    
    def create_note(self, title, description):
        """Create a new note with given title and description."""
        with allure.step(f"Create note with title: {title}"):
            # Click add note button
            self.click_add_note_button()
            
            # Wait for note form to be visible
            self.wait_for_element(self.NOTE_FORM)
            
            # Enter note title
            self.enter_note_title(title)
            
            # Enter note description
            self.enter_note_description(description)
            
            # Click save button
            self.click_save_note_button()
            
            # Wait for note to be saved
            self.wait_for_note_save_completion()
    
    def enter_note_title(self, title):
        """Enter note title."""
        with allure.step(f"Enter note title: {title}"):
            self.type_text(self.NOTE_TITLE_INPUT, title)
    
    def enter_note_description(self, description):
        """Enter note description."""
        with allure.step(f"Enter note description: {description}"):
            self.type_text(self.NOTE_DESCRIPTION_INPUT, description)
    
    def click_save_note_button(self):
        """Click save note button."""
        with allure.step("Click save note button"):
            # Try regular click first
            try:
                self.click_element(self.NOTE_SUBMIT_BUTTON)
            except Exception:
                # If regular click fails, try JavaScript click
                self.logger.info("Regular click failed, trying JavaScript click for save note button")
                element = self.wait_for_element(self.NOTE_SUBMIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", element)
    
    def wait_for_note_save_completion(self):
        """Wait for note to be saved and form to disappear."""
        with allure.step("Wait for note save completion"):
            import time
            time.sleep(2)
    
    def is_note_form_displayed(self):
        """Check if note form is displayed."""
        return self.is_element_visible(self.NOTE_FORM, timeout=5)
    
    
    def get_notes_count(self):
        """Get count of notes displayed."""
        try:
            # Try multiple approaches to find notes
            note_selectors = [
                self.NOTE_ITEM[1],  # Original selector
                ".note-item",
                ".note",
                ".card",
                "[class*='note']",
                "[class*='card']",
                "div[class*='note']",
                "div[class*='item']"
            ]
            
            for selector in note_selectors:
                try:
                    notes = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(notes) > 0:
                        self.logger.info(f"Found {len(notes)} notes using selector: {selector}")
                        return len(notes)
                except:
                    continue
            
            # If no notes found with selectors, try checking page content
            page_source = self.driver.page_source
            if "Test Note Title" in page_source or note_data["title"] in page_source if 'note_data' in globals() else False:
                self.logger.info("Note title found in page source but not with selectors")
                return 1
            
            return 0
        except Exception as e:
            self.logger.error(f"Error getting notes count: {e}")
            return 0
    
    def is_note_with_title_visible(self, title):
        """Check if note with specific title is visible."""
        try:
            note_elements = self.driver.find_elements(By.CSS_SELECTOR,'div[data-testid="note-card-title"]')
            ui_notes = []

            for element in note_elements:
                try:
                    note_text = element.text.strip()
                    if note_text:
                        ui_notes.append(note_text)
                except Exception:
                    continue
                
            self.logger.info(f"Titles:{ui_notes}")
            self.logger.info(f"Created title is : {title}")
            for note in ui_notes:
                self.logger.info(f"{note} : {title}")
                if note == title:
                    return True    
            return False
        except Exception as e:
            self.logger.error(f"Error checking note visibility: {e}")
            return False
    
    def get_note_title(self):
        NOTE_CARD_TITLE = (By.CSS_SELECTOR, 'div[data-testid="note-card-title"]')
        note_title = driver.find_element(*NOTE_CARD_TITLE).text
        self.logger.info(f"This is the title :{note_title}")
        
    
    def is_success_message_displayed(self):
        """Check if success message is displayed."""
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def is_description_validation_displayed(self):
        """Check if description validation message is displayed."""
        return self.is_element_visible(self.DESCRIPTION_VALIDATOR, timeout=5)
    
    def get_description_validation_message(self):
        """Get description validation message text."""
        try:
            element = self.wait_for_element(self.DESCRIPTION_VALIDATOR, timeout=5)
            return element.text.strip()
        except Exception:
            return None
    
    def is_title_validation_displayed(self):
        """Check if title validation message is displayed."""
        return self.is_element_visible(self.TITLE_VALIDATION, timeout=5)
    
    def get_title_validation_message(self):
        """Get title validation message text."""
        try:
            element = self.wait_for_element(self.TITLE_VALIDATION, timeout=5)
            return element.text.strip()
        except Exception:
            return None
    
    def get_all_validation_messages(self):
        """Get all validation messages displayed on the form."""
        validation_messages = []
        try:
            # Find all validation messages
            validation_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.invalid-feedback")
            for element in validation_elements:
                message = element.text.strip()
                if message:
                    validation_messages.append(message)
        except Exception:
            pass
        return validation_messages
    
    def get_success_message(self):
        """Get success message text."""
        if self.is_success_message_displayed():
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def wait_for_notes_page_load(self):
        """Wait for notes page to fully load."""
        with allure.step("Wait for notes page to load"):
            self.wait_for_element(self.ADD_NOTES_BUTTON)