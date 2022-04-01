from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from .db.models import Conference, Division, Player, Team
from .filters import (
    binary_column_filter,
    close_integer_column_filter,
    close_variable_column_filter,
    variable_column_filter
)
from .guess.context import BinaryAttributeContext, VariableAttributeContext, VariableCloseAttributeContext

"""
-- Exact layout of poeltl site
SELECT
    t.code,
    c.name,
    d.abbreviation,
    p.position,
    p.height_inches / 12 feet,
    p.height_inches % 12 inches,
    date_part('YEAR', age(CURRENT_DATE, p.birth_date)) age_,
    p.jersey_number
FROM players p
JOIN teams t ON p.team_id = t.id
JOIN divisions d ON t.division_id = d.id
JOIN conferences c ON d.conference_id = c.id
WHERE p.first_name = 'Josh' 
  AND p.last_name = 'Richardson';
"""

def build_query(
    team_code_context: VariableAttributeContext,
    conference_name_context: BinaryAttributeContext,
    division_abbreviation_context: VariableAttributeContext,
    player_position_context: VariableCloseAttributeContext,
    player_height_context: VariableCloseAttributeContext,
    player_age_context: VariableCloseAttributeContext,
    player_jersey_number_context: VariableCloseAttributeContext
):
    return (
        select(Player)
        .join(Player.team)
        .join(Team.division)
        .join(Division.conference)
        .where(
            variable_column_filter(
                Team.code,
                team_code_context.correct_value,
                team_code_context.incorrect_values
            ),
            binary_column_filter(
                Conference.name,
                conference_name_context.correct_value,
                conference_name_context.incorrect_value
            ),
            variable_column_filter(
                Division.abbreviation,
                division_abbreviation_context.correct_value,
                division_abbreviation_context.incorrect_values
            ),
            close_variable_column_filter(
                Player.position,
                player_position_context.correct_value,
                player_position_context.incorrect_values,
                None  # TODO: Use context.close_values to make real possible_values
            ),
            close_integer_column_filter(
                Player.height_inches,
                player_height_context.correct_value,
                player_height_context.incorrect_values,
                None  # TODO: Use context.close_values to make real possible_values
            ),
            close_integer_column_filter(
                func.date_part('YEAR', func.age(func.current_date(), Player.birth_date)),
                player_age_context.correct_value,
                player_age_context.incorrect_values,
                None  # TODO: Use context.close_values to make real possible_values
            ),
            close_integer_column_filter(
                Player.jersey_number,
                player_jersey_number_context.correct_value,
                player_jersey_number_context.incorrect_values,
                None  # TODO: Use context.close_values to make real possible_values
            )
        )
    )

# TODO: Delete this import used for test instantiation
from .guess.guesses import IntegerGuess, Direction

query = build_query(
    VariableAttributeContext(incorrect_values=['MIL']),  # Team.code
    BinaryAttributeContext(correct_value='East'),  # Conference.name
    VariableAttributeContext(incorrect_values=['Cen.']),  # Division.abbreviation
    VariableCloseAttributeContext(correct_value='G'),  # Player.position
    VariableCloseAttributeContext(incorrect_values=[IntegerGuess(77, Direction.HIGH)], close_values=[IntegerGuess(77, Direction.HIGH)]),  # Player.height_inches
    VariableCloseAttributeContext(correct_value=29),  # Player.birth_date 
    VariableCloseAttributeContext(incorrect_values=[IntegerGuess(24, Direction.HIGH)])  # Player.jersey_number
)

engine = create_engine('postgresql://postgres@localhost/poeltl')

with Session(engine) as session:    
    # Using the normal session.execute(query) returns each player as a single item in a row.
    # The sqlalchemy documentation recommends using session.scalars() to avoid calling row[0] to get each player object
    players = session.scalars(query).all()
    for player in players:
        print(player)
