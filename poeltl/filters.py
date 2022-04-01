from typing import Any, List

from sqlalchemy import and_, Column

from .guess.guesses import Direction, IntegerGuess


def binary_column_filter(column: Column, correct_guess: Any, incorrect_guess: Any):
    if correct_guess:
        return column == correct_guess
    
    if incorrect_guess:
        return column != incorrect_guess
    
    return True


def variable_column_filter(column: Column, correct_guess: Any, incorrect_guesses: List[Any]):
    if correct_guess:
        return column == correct_guess
    
    if incorrect_guesses:
        return column.notin_(incorrect_guesses)
    
    return True


def close_integer_column_filter(column: Column, correct_guess: int, incorrect_guesses: List[IntegerGuess], possible_values: List[int]):
    if correct_guess:
        return column == correct_guess

    # There will only be possible values if there is at least one incorrect guess
    if possible_values:
        return and_(
            _get_min_and_or_max_integer_filter(column, *_get_min_and_max_integer_guess_values(incorrect_guesses)),
            column.in_(possible_values)
        )
    
    if incorrect_guesses:
        _get_min_and_or_max_integer_filter(column, *_get_min_and_max_integer_guess_values(incorrect_guesses))

    return True


def close_variable_column_filter(column: Column, correct_guess: Any, incorrect_guesses: List[Any], possible_values: List[Any]):
    if correct_guess:
        return column == correct_guess
    
    # There will only be possible values if there is at least one incorrect guess
    if possible_values:
        return and_(column.notin_(incorrect_guesses), column.in_(possible_values))

    if incorrect_guesses:
        return column.notin_(incorrect_guesses)
    
    return True


def _get_min_and_or_max_integer_filter(column: Column, min_value: int, max_value: int):
    if min_value and max_value:
        return and_(column > min_value, column < max_value)
    elif min_value:
        return column > min_value
    elif max_value:
        return column < max_value


def _get_min_and_max_integer_guess_values(guesses: List[IntegerGuess]):
    
    low_guesses = []
    high_guesses = []

    for guess in guesses:
        if guess.direction is Direction.LOW:
            low_guesses.append(guess)
        elif guess.direction is Direction.HIGH:
            high_guesses.append(guess)
        else:
            raise ValueError(f"Unsupported IntegerGuess direction: {guess.direction}")

    max_low_value = None
    if low_guesses:
        max_low_value = max(guess.value for guess in low_guesses)
    
    min_high_value = None
    if high_guesses:
        min_high_value = min(guess.value for guess in high_guesses)

    return max_low_value, min_high_value
