from dataclasses import dataclass
from enum import auto, Enum, unique

from .value import AttributeValue


@unique
class AttributeStatus(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    CLOSE = auto()


@dataclass
class AttributeFeedback:
    value: AttributeValue
    status: AttributeStatus


@dataclass
class GuessFeedback:
    team_code_feedback: AttributeFeedback
    conference_name_feedback: AttributeFeedback
    division_abbreviation_feedback:  AttributeFeedback
    player_position_feedback: AttributeFeedback
    player_height_inches_feedback: AttributeFeedback
    player_age_feedback: AttributeFeedback
    player_jersey_number_feedback: AttributeFeedback
