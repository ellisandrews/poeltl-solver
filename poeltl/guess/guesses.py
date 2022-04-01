from enum import auto, Enum, unique


class PlayerPositionGuess:

    def __init__(self, position: str):
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: str):
        self._position = value


@unique
class Direction(Enum):
    LOW = auto()
    HIGH = auto()


class IntegerGuess:

    def __init__(self, value: int, direction: Direction = None):
        self._value = value
        self._direction = direction

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: Direction):
        self._direction = value
