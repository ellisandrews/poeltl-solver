from dataclasses import dataclass
from enum import auto, Enum, unique

from typing import Any


@unique
class Direction(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass
class AttributeValue:
    value: Any = None


@dataclass
class IntegerAttributeValue(AttributeValue):
    direction: Direction = None
