from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .guess.feedback import AttributeFeedback, AttributeStatus, GuessFeedback
from .guess.value import AttributeValue, Direction, IntegerAttributeValue


class Guesser:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def navigate_to_poeltl_site(self):
        # Navigate to the site
        self.driver.get('https://poeltl.dunk.town/')

        # Close the modal explaining the game
        wait = WebDriverWait(self.driver, 5)
        close_modal_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='how-to-play']/following-sibling::button")))
        close_modal_button.click()

    def execute_guess(self, player_name: str):
        # Enter the player name guess into the text field and hit enter
        # TODO: Add some retry logic / validation if the player guess isn't found
        input_element = self.driver.find_element(By.XPATH, "//input[@type='text']")
        input_element.send_keys(player_name)
        input_element.send_keys(Keys.RETURN)
        
        # If the value is still present after sending ENTER the player was not found
        if input_element.get_attribute('value'):
            print(f"Player not found in the UI: {player_name}")
            input_element.clear()
            return False

        return True

    def get_most_recent_guess_feedback(self) -> GuessFeedback:

        table_rows = self.driver.find_elements(By.XPATH, "//div[@class='game-table__body']/div[contains(@class, 'game-table__row')]")

        if len(table_rows) == 0:
            raise ValueError('No player guess table rows found')

        most_recent_row = table_rows[-1]
        most_recent_row_cells = most_recent_row.find_elements(By.XPATH, "div[contains(@class, 'game-table__cell')]")

        if len(most_recent_row_cells) != 8:
            raise ValueError(f"Found unexpected number of row cells: {len(most_recent_row_cells)}")

        guess_feedback = GuessFeedback()

        for column, cell in zip(
                ['name', 'team', 'conference', 'division', 'position', 'height', 'age', 'number'],
                most_recent_row_cells
            ):            
            
            # Determine attribute status from HTML tag class
            class_ = cell.get_attribute('class')
            if 'green' in class_:
                attribute_status = AttributeStatus.CORRECT
            elif 'yellow' in class_:
                attribute_status = AttributeStatus.CLOSE
            else:
                attribute_status = AttributeStatus.INCORRECT

            # Grab the plaintext value of the row cell
            value = cell.find_element(By.XPATH, "div/div[contains(@class, 'text')]").text
            if not value:
                raise ValueError(f"No cell value found for table column: {column}") 

            # Build the correct AttributeValue object
            if column in ('height', 'age', 'number'):

                # Correct guesses will not have a direction
                try:
                    raw_direction = cell.find_element(By.XPATH, "div/div[contains(@class, 'dir')]").text
                except NoSuchElementException:
                    raw_direction = None

                direction = None
                if raw_direction == '↓':
                    direction = Direction.HIGH
                elif raw_direction == '↑':
                    direction = Direction.LOW
                
                if column == 'height':
                    int_value = self._convert_raw_height_string_to_inches(value)
                else:
                    int_value = int(value)                
                
                attribute_value = IntegerAttributeValue(int_value, direction)            
            
            else:
                attribute_value = AttributeValue(value)

            # Build the feedback object
            attribute_feedback = AttributeFeedback(attribute_value, attribute_status)

            # Assign the feedback object to the correct feeback attribute
            if column == 'name':
                guess_feedback.player_name_feedback = attribute_feedback
            elif column == 'team':
                guess_feedback.team_code_feedback = attribute_feedback
            elif column == 'conference':
                guess_feedback.conference_name_feedback = attribute_feedback
            elif column == 'division':
                guess_feedback.division_abbreviation_feedback = attribute_feedback
            elif column == 'position':
                guess_feedback.player_position_feedback = attribute_feedback
            elif column == 'height':
                guess_feedback.player_height_inches_feedback = attribute_feedback
            elif column == 'age':
                guess_feedback.player_age_feedback = attribute_feedback
            elif column == 'number':
                guess_feedback.player_jersey_number_feedback = attribute_feedback
            else:
                raise ValueError(f"Unsupported table column: {column}")

        return guess_feedback

    @staticmethod
    def _convert_raw_height_string_to_inches(raw_string) -> int:
        # Converts string like 6'7" --> 79 (integer inches)
        raw_feet, raw_inches = raw_string.split('\'')
        return int(raw_feet) * 12 + int(raw_inches.replace('"', ''))
