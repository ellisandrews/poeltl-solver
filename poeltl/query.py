from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .db.models import Division, Player, Team
from .filters import (
    conference_name_filter,
    division_abbreviation_filter,
    player_age_filter,
    player_height_inches_filter,
    player_jersey_number_filter,
    player_position_filter,
    team_code_filter
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
            team_code_filter(
                team_code_context.correct_value,
                team_code_context.incorrect_values
            ),
            conference_name_filter(
                conference_name_context.correct_value,
                conference_name_context.incorrect_value
            ),
            division_abbreviation_filter(
                division_abbreviation_context.correct_value,
                division_abbreviation_context.incorrect_values
            ),
            player_position_filter(
                player_position_context.correct_value,
                player_position_context.incorrect_values,
                player_position_context.close_values
            ),
            player_height_inches_filter(
                player_height_context.correct_value,
                player_height_context.incorrect_values,
                player_height_context.close_values
            ),
            player_age_filter(
                player_age_context.correct_value,
                player_age_context.incorrect_values,
                player_age_context.close_values
            ),
            player_jersey_number_filter(
                player_jersey_number_context.correct_value,
                player_jersey_number_context.incorrect_values,
                player_jersey_number_context.close_values
            )
        )
    )


query = build_query(
    # TODO
)

engine = create_engine('postgresql://postgres@localhost/poeltl')

with Session(engine) as session:    
    # Using the normal session.execute(query) returns each player as a single item in a row.
    # The sqlalchemy documentation recommends using session.scalars() to avoid calling row[0] to get each player object
    players = session.scalars(query).all()
    for player in players:
        print(player)
