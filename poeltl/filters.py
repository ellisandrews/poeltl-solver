from typing import List

from sqlalchemy import and_, func

from .db.models import Conference, Division, Player, Team
from .guess.guesses import Direction, PlayerAgeGuess, PlayerHeightGuess, PlayerJerseyNumberGuess, PlayerPositionGuess


def team_code_filter(correct_guess: str, incorrect_guesses: List[str]):
    if correct_guess:
        return Team.code == correct_guess
    
    if incorrect_guesses:
        return Team.code.notin_(incorrect_guesses)
    
    return True


def conference_name_filter(correct_guess: str, incorrect_guess: str):
    if correct_guess:
        return Conference.name == correct_guess
    
    if incorrect_guess:
        return Conference.name != incorrect_guess
    
    return True


def division_abbreviation_filter(correct_guess: str, incorrect_guesses: List[str]):
    if correct_guess:
        return Division.abbreviation == correct_guess
    
    if incorrect_guesses:
        return Division.abbreviation.notin_(incorrect_guesses)
    
    return True


# TODO: Consider making a PlayerPositionGuess object that knows about the close positions?
# TODO: Make close positions acutally smart here
def player_position_filter(correct_guess: str, incorrect_guesses: List[PlayerPositionGuess], close_guesses: List[PlayerPositionGuess]):
    if correct_guess:
        return Player.position == correct_guess
    
     # NOTE: close is a subset of incorrect
    if close_guesses:
        return and_(Player.position.notin_([guess.position for guess in incorrect_guesses]), Player.position.in_(_get_possible_player_positions(close_guesses)))

    if incorrect_guesses:
        return Player.position.notin_([guess.position for guess in incorrect_guesses])
    
    return True


# TODO: Figure out how to make close guesses work
def player_height_inches_filter(correct_guess: int, incorrect_guesses: List[PlayerHeightGuess], close_guesses: List[PlayerHeightGuess]):
    if correct_guess:
        return Player.height_inches == correct_guess
    
    if incorrect_guesses:
        incorrect_low_guesses = []
        incorrect_high_guesses = []
        for guess in incorrect_guesses:
            if guess.direction is Direction.LOW:
                incorrect_low_guesses.append(guess)
            elif guess.direction is Direction.HIGH:
                incorrect_high_guesses.append(guess)
            else:
                raise ValueError(f"Unsupported PlayerHeightGuess direction: {guess.direction}")

        if incorrect_low_guesses:
            max_low_inches = max(guess.inches for guess in incorrect_low_guesses)
        
        if incorrect_high_guesses:
            min_high_inches = min(guess.inches for guess in incorrect_high_guesses)

     # NOTE: close is a subset of incorrect
    if close_player_heights:
        return and_(Player.height_inches.notin_(incorrect_player_heights), Player.height_inches.in_(_get_possible_player_height_inches(close_player_heights)))

    if incorrect_player_heights:
        return Player.height_inches.notin_([close_player_height.height_inches for close_player_height in close_player_heights])
    
    return True
    return Player.height_inches < 83


def player_age_filter():
    return func.date_part('YEAR', func.age(func.current_date(), Player.birth_date)) < 26


def player_jersey_number_filter():
    return Player.jersey_number > 32


# TODO: Implement
def _get_possible_player_positions(close_guesses: List[PlayerPositionGuess]):
    return ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C']  # These are all the positions


# TODO: Implement
def _get_possible_player_height_inches(close_player_heights):
    return list(range(0, 100))
