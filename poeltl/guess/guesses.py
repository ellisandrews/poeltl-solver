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


class PlayerHeightGuess(IntegerGuess):
    
    def __init__(self, inches: int = None, direction: Direction = None):
        super().__init__(inches, direction)
    
    @property
    def inches(self):
        return super().value

    @inches.setter
    def inches(self, value: int):
        super().value = value


class PlayerAgeGuess(IntegerGuess):
    
    def __init__(self, age: int = None, direction: Direction = None):
        super().__init__(age, direction)

    @property
    def age(self):
        return super().value

    @age.setter
    def age(self, value: int):
        super().value = value


class PlayerJerseyNumberGuess(IntegerGuess):
    
    def __init__(self, jersey_number: int = None, direction: Direction = None):
        super().__init__(jersey_number, direction)
        
    @property
    def jersey_number(self):
        return super().value

    @jersey_number.setter
    def jersey_number(self, value: int):
        super().value = value
