from .guess.feedback import AttributeFeedback, AttributeStatus, GuessFeedback
from .guess.value import AttributeValue, Direction, IntegerAttributeValue


class Guesser:

    # TODO: Implement instead of returning static data
    def execute_guess(self, player_name: str) -> GuessFeedback:
        if player_name == 'Zach Collins':
            return GuessFeedback(
                team_code_feedback = AttributeFeedback(AttributeValue('SAS'), AttributeStatus.INCORRECT),
                conference_name_feedback = AttributeFeedback(AttributeValue('West'), AttributeStatus.INCORRECT),
                division_abbreviation_feedback = AttributeFeedback(AttributeValue('SW'), AttributeStatus.INCORRECT),
                player_position_feedback = AttributeFeedback(AttributeValue('F-C'), AttributeStatus.CLOSE),
                player_height_inches_feedback = AttributeFeedback(IntegerAttributeValue(83, Direction.HIGH), AttributeStatus.CLOSE),
                player_age_feedback = AttributeFeedback(IntegerAttributeValue(24, Direction.LOW), AttributeStatus.CLOSE),
                player_jersey_number_feedback = AttributeFeedback(IntegerAttributeValue(23, Direction.LOW), AttributeStatus.INCORRECT)
            )
        elif player_name == 'Juancho Hernangomez':
            return GuessFeedback(
                team_code_feedback = AttributeFeedback(AttributeValue('UTA'), AttributeStatus.INCORRECT),
                conference_name_feedback = AttributeFeedback(AttributeValue('West'), AttributeStatus.INCORRECT),
                division_abbreviation_feedback = AttributeFeedback(AttributeValue('NW'), AttributeStatus.INCORRECT),
                player_position_feedback = AttributeFeedback(AttributeValue('F'), AttributeStatus.CORRECT),
                player_height_inches_feedback = AttributeFeedback(IntegerAttributeValue(81), AttributeStatus.CORRECT),
                player_age_feedback = AttributeFeedback(IntegerAttributeValue(26), AttributeStatus.CORRECT),
                player_jersey_number_feedback = AttributeFeedback(IntegerAttributeValue(41, Direction.HIGH), AttributeStatus.INCORRECT)
            )
        