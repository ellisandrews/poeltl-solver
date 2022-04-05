from dataclasses import dataclass
from enum import auto, Enum, unique

from poeltl.guess.value import AttributeValue


@unique
class AttributeStatus(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    CLOSE = auto()


@dataclass
class AttributeFeedback:
    value: AttributeValue = None
    status: AttributeStatus = None


@dataclass
class GuessFeedback:
    player_name_feedback: AttributeFeedback = None
    team_code_feedback: AttributeFeedback = None
    conference_name_feedback: AttributeFeedback = None
    division_abbreviation_feedback:  AttributeFeedback = None
    player_position_feedback: AttributeFeedback = None
    player_height_inches_feedback: AttributeFeedback = None
    player_age_feedback: AttributeFeedback = None
    player_jersey_number_feedback: AttributeFeedback = None
