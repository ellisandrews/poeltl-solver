from sqlalchemy import and_, Column

from .guess.context import (
    BinaryAttributeContext,
    IntegerAttributeContext,
    PositionAttributeContext,
    VariableAttributeContext,
    VariableCloseAttributeContext
)
from .guess.value import AttributeValue, Direction, IntegerAttributeValue


# TODO: Empirically test that this mapping of position feedback --> possible correct position is correct
_CLOSE_POSITIONS_MAP = {
    'G':   {'G-F', 'F-G'},
    'G-F': {'G', 'F-G', 'F'},
    'F-G': {'G', 'G-F', 'F'},
    'F':   {'F-G', 'F-C'},
    'F-C': {'F', 'C-F'},
    'C-F': {'F', 'F-C', 'C'},
    'C':   {'F-C', 'C-F'}
}

_CLOSE_INTEGER_DISTANCE = 2


def binary_column_filter(column: Column, context: BinaryAttributeContext):
    if context.correct_value:
        return _correct_value_filter(column, context.correct_value)
    
    if context.incorrect_value:
        return _incorrect_value_filter(column, context.incorrect_value)
    
    return True


def variable_column_filter(column: Column, context: VariableAttributeContext):
    if context.correct_value:
        return _correct_value_filter(column, context.correct_value)
    
    if context.incorrect_values:
        return _incorrect_values_filter(column, context.incorrect_values)
    
    return True


def variable_close_column_filter(column: Column, context: VariableCloseAttributeContext):
    if context.correct_value:
        return _correct_value_filter(column, context.correct_value)
    
    if isinstance(context, PositionAttributeContext):
        _incorrect_filter = _incorrect_values_filter
        _close_filter = _close_position_values_filter
    elif isinstance(context, IntegerAttributeContext):
        _incorrect_filter = _integer_values_filter
        _close_filter = _close_integer_values_filter
    else:
        raise ValueError(f"Unsupported context type: {type(context).__name__}")

    if context.incorrect_values and context.close_values:
        return and_(
            _incorrect_filter(column, context.incorrect_values),
            _close_filter(column, context.close_values)
        )

    if context.incorrect_values:
        return _incorrect_filter(column, context.incorrect_values)

    if context.close_values:
        return _close_filter(column, context.close_values)

    return True


def _correct_value_filter(column: Column, correct_value: AttributeValue):
    return column == correct_value.value


def _incorrect_value_filter(column: Column, incorrect_value: AttributeValue):
    return column != incorrect_value.value


def _incorrect_values_filter(column: Column, incorrect_values: list[AttributeValue]):
    return column.notin_([incorrect_value.value for incorrect_value in incorrect_values])


def _close_position_values_filter(column: Column, close_values: list[AttributeValue]):
    possible_position_sets = [_CLOSE_POSITIONS_MAP[close_value.value] for close_value in close_values]
    possible_positions = set().union(*possible_position_sets)
    return column.in_(list(possible_positions)) 


def _close_integer_values_filter(column: Column, close_values: list[IntegerAttributeValue]):
    possible_value_sets = []
    for close_value in close_values:
        if close_value.direction is Direction.LOW:
            possible_value_sets.append(set(range(close_value.value + 1, close_value.value + _CLOSE_INTEGER_DISTANCE + 1)))
        elif close_value.direction is Direction.HIGH:
            possible_value_sets.append(set(range(close_value.value - _CLOSE_INTEGER_DISTANCE, close_value.value)))
        else:
            raise ValueError(f"Unsupported direction: {close_value.direction}")
    possible_values = set().union(*possible_value_sets)
    return column.in_(list(possible_values)) 


def _integer_values_filter(column: Column, close_values: list[IntegerAttributeValue]):
    return _get_min_and_or_max_integer_filter(column, *_get_min_and_max_integer_values(close_values))


def _get_min_and_or_max_integer_filter(column: Column, min_value: int, max_value: int):
    if min_value and max_value:
        return and_(column > min_value, column < max_value)
    elif min_value:
        return column > min_value
    elif max_value:
        return column < max_value
    else:
        raise ValueError('Must specify at least one of [min_value, max_value]')


def _get_min_and_max_integer_values(integer_attribute_values: list[IntegerAttributeValue]):
    
    low_values = []
    high_values = []

    for integer_attribute_value in integer_attribute_values:
        if integer_attribute_value.direction is Direction.LOW:
            low_values.append(integer_attribute_value)
        elif integer_attribute_value.direction is Direction.HIGH:
            high_values.append(integer_attribute_value)
        else:
            raise ValueError(f"Unsupported direction: {integer_attribute_value.direction}")

    max_low_value = None
    if low_values:
        max_low_value = max(integer_attribute_value.value for integer_attribute_value in low_values)
    
    min_high_value = None
    if high_values:
        min_high_value = min(integer_attribute_value.value for integer_attribute_value in high_values)

    return max_low_value, min_high_value
