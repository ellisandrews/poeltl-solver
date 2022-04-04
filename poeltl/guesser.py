from selenium import webdriver
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


    # TODO: Implement instead of returning static data
    def execute_guess(self, player_name: str) -> GuessFeedback:
        # Enter the guess into the input text field
        # TODO: Add some retry logic / validation if the player guess isn't found
        input_element = self.driver.find_element_by_xpath("//input[@type='text']")
        input_element.send_keys(player_name)
        input_element.send_keys(Keys.RETURN)

        


        # if player_name == 'Zach Collins':
        #     return GuessFeedback(
        #         team_code_feedback = AttributeFeedback(AttributeValue('SAS'), AttributeStatus.INCORRECT),
        #         conference_name_feedback = AttributeFeedback(AttributeValue('West'), AttributeStatus.INCORRECT),
        #         division_abbreviation_feedback = AttributeFeedback(AttributeValue('SW'), AttributeStatus.INCORRECT),
        #         player_position_feedback = AttributeFeedback(AttributeValue('F-C'), AttributeStatus.CLOSE),
        #         player_height_inches_feedback = AttributeFeedback(IntegerAttributeValue(83, Direction.HIGH), AttributeStatus.CLOSE),
        #         player_age_feedback = AttributeFeedback(IntegerAttributeValue(24, Direction.LOW), AttributeStatus.CLOSE),
        #         player_jersey_number_feedback = AttributeFeedback(IntegerAttributeValue(23, Direction.LOW), AttributeStatus.INCORRECT)
        #     )
        # elif player_name == 'Juancho Hernangomez':
        #     return GuessFeedback(
        #         team_code_feedback = AttributeFeedback(AttributeValue('UTA'), AttributeStatus.INCORRECT),
        #         conference_name_feedback = AttributeFeedback(AttributeValue('West'), AttributeStatus.INCORRECT),
        #         division_abbreviation_feedback = AttributeFeedback(AttributeValue('NW'), AttributeStatus.INCORRECT),
        #         player_position_feedback = AttributeFeedback(AttributeValue('F'), AttributeStatus.CORRECT),
        #         player_height_inches_feedback = AttributeFeedback(IntegerAttributeValue(81), AttributeStatus.CORRECT),
        #         player_age_feedback = AttributeFeedback(IntegerAttributeValue(26), AttributeStatus.CORRECT),
        #         player_jersey_number_feedback = AttributeFeedback(IntegerAttributeValue(41, Direction.HIGH), AttributeStatus.INCORRECT)
        #     )
        