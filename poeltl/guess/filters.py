from sqlalchemy import and_, Column

from poeltl.guess.context import (
    BinaryAttributeContext,
    IntegerAttributeContext,
    PositionAttributeContext,
    VariableAttributeContext,
    VariableCloseAttributeContext
)
from poeltl.guess.value import AttributeValue, Direction, IntegerAttributeValue


# TODO: Empirically test that this mapping of close position feedback --> possible correct position is correct
_CLOSE_POSITIONS_MAP = {
    'G':   {'G-F', 'F-G'},
    'G-F': {'G', 'F-G', 'F'},
    'F-G': {'G', 'G-F', 'F'},
    'F':   {'F-G', 'F-C'},
    'F-C': {'F', 'C-F', 'C'},
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
        incorrect_filter = _incorrect_position_values_filter
        close_filter = _close_position_values_filter
    elif isinstance(context, IntegerAttributeContext):
        incorrect_filter = _incorrect_integer_values_filter
        close_filter = _close_integer_values_filter
    else:
        raise ValueError(f"Unsupported context type: {type(context).__name__}")

    if context.incorrect_values and context.close_values:
        return and_(
            incorrect_filter(column, context.incorrect_values),
            close_filter(column, context.close_values)
        )

    if context.incorrect_values:
        return incorrect_filter(column, context.incorrect_values)

    if context.close_values:
        return close_filter(column, context.close_values)

    return True


def _correct_value_filter(column: Column, correct_value: AttributeValue):
    return column == correct_value.value


def _incorrect_value_filter(column: Column, incorrect_value: AttributeValue):
    return column != incorrect_value.value


def _incorrect_values_filter(column: Column, incorrect_values: list[AttributeValue]):
    return column.notin_([incorrect_value.value for incorrect_value in incorrect_values])


def _incorrect_position_values_filter(column: Column, incorrect_values: list[AttributeValue]):
    incorrect_positions = set()
    for incorrect_value in incorrect_values:
        incorrect_positions.add(incorrect_value.value)
        # If the observed INCORRECT value is in the possible values set for a given close_value key,
        # then the close_value key can be ruled out as INCORRECT because it otherwise would have registered as CLOSE
        for close_value, possible_values in _CLOSE_POSITIONS_MAP.items():
            if incorrect_value.value in possible_values:
                incorrect_positions.add(close_value)
    return column.notin_(list(incorrect_positions))


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


def _incorrect_integer_values_filter(column: Column, close_values: list[IntegerAttributeValue]):
    return _get_min_and_or_max_integer_filter(column, *_get_min_and_max_integer_values(close_values))


def _get_min_and_or_max_integer_filter(column: Column, min_value: int, max_value: int):
    if min_value is not None and max_value is not None:
        return and_(column > min_value, column < max_value)
    elif min_value is not None:
        return column > min_value
    elif max_value is not None:
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
        max_low_value = max(integer_attribute_value.value for integer_attribute_value in low_values) + _CLOSE_INTEGER_DISTANCE

    min_high_value = None
    if high_values:
        min_high_value = min(integer_attribute_value.value for integer_attribute_value in high_values) - _CLOSE_INTEGER_DISTANCE

    return max_low_value, min_high_value
