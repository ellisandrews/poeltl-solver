from enum import auto, Enum, unique


@unique
class AttributeStatus(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    CLOSE = auto()


@unique
class Direction(Enum):
    LOW = auto()
    HIGH = auto()


class AttributeFeedback:

    def __init__(self, value, status):
        if not isinstance(status, AttributeStatus):
            raise ValueError(f"Unsupported status: {status}")
        self.value = value
        self.status = status


class NumericAttributeFeedback(AttributeFeedback):
    
    def __init__(self, value, status, direction):
        super().__init__(value, status)
        if not isinstance(direction, Direction):
            raise ValueError(f"Unsupported direction: {direction}")
        self.direction = direction


class AttributeFeedbackStore:
    
    def __init__(self):
        self.correct = None
        self.incorrect = []
        self.close = []

    def add_attribute_feedback(self, value, status):
        if status is AttributeStatus.CORRECT:
            self.correct = value
        elif status is AttributeStatus.INCORRECT:
            self.incorrect.append(value)
        elif status is AttributeStatus.CLOSE:
            self.close.append(value)
        else:
            raise ValueError(f"Unsupported status: {status}")


class NumericAttributeFeedbackStore(AttributeFeedbackStore):

    def add_attribute_feedback(self, value, status, direction):
        if status is AttributeStatus.CORRECT:
            self.correct = value
        elif status is AttributeStatus.INCORRECT:
            self.incorrect.append((value, direction))
        else:
            self.close.append((value, direction))


class GuessFeedback:

    def __init__(
        self,
        team,
        conference,
        division,
        position,
        height_inches,
        age,
        jersery_number
    ):
        self.team = team
        self.conference = conference
        self.division = division
        self.position = position
        self.height_inches = height_inches
        self.age = age
        self.jersey_number = jersery_number


class GuessFeedbackStore:

    def __init__(self):
        self.players = []
        self.team = AttributeFeedbackStore()
        self.conference = AttributeFeedbackStore()
        self.division = AttributeFeedbackStore()
        self.position = AttributeFeedbackStore()
        self.height_inches = NumericAttributeFeedbackStore()
        self.age = NumericAttributeFeedbackStore()
        self.jersey_number = NumericAttributeFeedbackStore()

    def add_guess_feedback(
        player,
        team,
        conference,
        division,
        position,
        height_inches,
        age,
        jersey_number
    ):
        pass

    
