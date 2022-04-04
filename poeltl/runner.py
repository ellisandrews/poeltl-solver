from curses import echo
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .guess.context import GameContext
from .guess.mapping import map_feedback_to_context
from .guesser import Guesser
from .query import build_query


guesser = Guesser()
guesser.navigate_to_poeltl_site()
guesser.execute_guess('Zach Collins')


# 1. Get a random player from the database and guess their name
# 2. Execute the guess and get feedback for each attribute on the guess
# 3. Translate feedback to context
# 4. Build a query for next player guess from the updated game context

# # Example with a couple of guesses

# game_context = GameContext()

# guess_feedback = guesser.execute_guess('Zach Collins')
# game_context = map_feedback_to_context(guess_feedback, game_context)

# guess_feedback = guesser.execute_guess('Juancho Hernangomez')
# game_context = map_feedback_to_context(guess_feedback, game_context)

# # Query based on a couple of guesses
# player_query = build_query(game_context)
# engine = create_engine('postgresql://postgres@localhost/poeltl', echo=True)
# with Session(engine) as session:    
#     # Using the normal session.execute(query) returns each player as a single item in a row.
#     # The sqlalchemy documentation recommends using session.scalars() to avoid calling row[0] to get each player object
#     players = session.scalars(player_query).all()
#     for player in players:
#         print(player)
