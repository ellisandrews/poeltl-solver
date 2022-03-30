from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from poeltl.db.models.conference import Conference

from .db.models import Conference, Division, Player, Team


incorrect_team_codes = ['MIN']
correct_conference_name = 'West'
correct_division_abbreviation = 'NW'
close_player_positions = ['C', 'F-C', 'F']
high_player_height_inches = 83
high_player_age = 26
low_player_jersey_number = 32

statement = (
    select(Player).
    join(Player.team).
    join(Team.division).
    join(Division.conference).
    where(
        Team.code.notin_(incorrect_team_codes),
        Conference.name == correct_conference_name,
        Division.abbreviation == correct_division_abbreviation,
        Player.position.in_(close_player_positions),
        Player.height_inches < high_player_height_inches,
        func.date_part('YEAR', func.age(func.current_date(), Player.birth_date)) < 26,
        Player.jersey_number > low_player_jersey_number
    )
)

engine = create_engine('postgresql://postgres@localhost/poeltl')

with Session(engine) as session:
    for row in session.execute(statement):
        print(row)

"""
SELECT p.*
FROM players p
JOIN teams t ON p.team_id = t.id
JOIN divisions d ON t.division_id = d.id
JOIN conferences c ON d.conference_id = c.id
WHERE t.code NOT IN ('MIN')
  AND c.name = 'West'
  AND d.name = 'Northwest'
  AND p.position IN ('C', 'F-C', 'F')
  AND p.height_inches < 83
  AND date_part('year', AGE(CURRENT_DATE, p.birth_date)) < 26
  AND p.jersey_number > 32;
"""


# from feedback import AttributeFeedback, AttributeStatus, GuessFeedback, NumericAttributeFeedback

# # 1. Guess a player name
# # 2. Create GuessFeedback
# # 3. Assimilate GuessFeedback to store of all GuessFeedback
# #      - This should also track already guessed players
# # 4. Use store of all GuessFeedback to create a DB query for possible next players to guess
# # 5. Grab a player name returned from the database query to guess next



# player_name = 'Andrew Wiggins'

# # Do the guess

# # Create feedback from guess


# returned_data = (
    
# )


# guess_feedback = GuessFeedback(
#     AttributeFeedback('GSW', AttributeStatus.INCORRECT),
#     AttributeFeedback('West', AttributeStatus.INCORRECT),
#     AttributeFeedback('Pac.', AttributeStatus.INCORRECT),
#     AttributeFeedback('F', AttributeStatus.CLOSE),
#     NumericAttributeFeedback(79, AttributeStatus.INCORRECT, Direction.LOW),
#     NumericAttributeFeedback(27, AttributeStatus.CLOSE, Direction.LOW),
#     NumericAttributeFeedback(22, AttributeStatus.INCORRECT, Direction.LOW)
# )
