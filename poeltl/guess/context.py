from dataclasses import dataclass, field

from .value import AttributeValue, IntegerAttributeValue


@dataclass
class AttributeContext:
    correct_value: AttributeValue = None


@dataclass
class BinaryAttributeContext(AttributeContext):
    incorrect_value: AttributeValue = None


@dataclass
class VariableAttributeContext(AttributeContext):
    incorrect_values: list[AttributeValue] = field(default_factory=list)


@dataclass
class VariableCloseAttributeContext(VariableAttributeContext):
    close_values: list[AttributeValue] = field(default_factory=list)


@dataclass
class IntegerAttributeContext(VariableCloseAttributeContext):
    close_values: list[IntegerAttributeValue] = field(default_factory=list)


@dataclass
class PositionAttributeContext(VariableCloseAttributeContext):
    pass


@dataclass
class GameContext:
    team_code_context: VariableAttributeContext = field(default_factory=lambda: VariableAttributeContext())
    conference_name_context: BinaryAttributeContext = field(default_factory=lambda: BinaryAttributeContext())
    division_abbreviation_context: VariableAttributeContext = field(default_factory=lambda: VariableAttributeContext())
    player_position_context: VariableCloseAttributeContext = field(default_factory=lambda: PositionAttributeContext())
    player_height_inches_context: VariableCloseAttributeContext = field(default_factory=lambda: IntegerAttributeContext())
    player_age_context: VariableCloseAttributeContext = field(default_factory=lambda: IntegerAttributeContext())
    player_jersey_number_context: VariableCloseAttributeContext = field(default_factory=lambda: IntegerAttributeContext())
