
from sqlalchemy import func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select

from poeltl.db.models import Conference, Division, Player, Team
from poeltl.guess.context import GameContext
from poeltl.guess.filters import binary_column_filter, variable_close_column_filter, variable_column_filter


class QueryManager:

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def build_query(game_context: GameContext) -> Select:
        return (
            select(Player)
            .join(Player.team)
            .join(Team.division)
            .join(Division.conference)
            .where(
                variable_column_filter(
                    Team.code,
                    game_context.team_code_context
                ),
                binary_column_filter(
                    Conference.name,
                    game_context.conference_name_context
                ),
                variable_column_filter(
                    Division.abbreviation,
                    game_context.division_abbreviation_context
                ),
                variable_close_column_filter(
                    Player.position,
                    game_context.player_position_context
                ),
                variable_close_column_filter(
                    Player.height_inches,
                    game_context.player_height_inches_context
                ),
                variable_close_column_filter(
                    func.date_part('YEAR', func.age(func.current_date(), Player.birth_date)),
                    game_context.player_age_context
                ),
                variable_close_column_filter(
                    Player.jersey_number,
                    game_context.player_jersey_number_context
                )
            )
            .order_by(func.random())
        )

    def execute_query(self, query: Select):
        # Using the normal session.execute(query) returns each Player as a single item in a row.
        # The sqlalchemy documentation recommends using session.scalars() to avoid calling row[0] to get each Player object
        with Session(self.engine) as session:    
            return session.scalars(query).all()
