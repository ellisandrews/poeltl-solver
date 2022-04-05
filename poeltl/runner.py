from time import sleep

from sqlalchemy import create_engine

from .guess.context import GameContext
from .guess.feedback import AttributeStatus
from .guess.mapping import map_feedback_to_context
from .guesser import Guesser
from .query import build_query, execute_query


# Connect to the database
engine = create_engine('postgresql://postgres@localhost/poeltl')

# Instantiate long-lived objects
guesser = Guesser()
game_context = GameContext()

# Launch a web browser and navigate to the game site
guesser.navigate_to_poeltl_site()

# Execute main game loop until the game is solved
solved = False
attempts = 0

while not solved:

    # Increment the attempts counter
    attempts += 1

    print(f"Beginning attempt {attempts}")

    # Query the database for a possible player to guess based on known context
    query = build_query(game_context)
    players = execute_query(engine, query)
    
    # Try players one by one until a successful guess is submitted
    guess_succeeded = False
    while not guess_succeeded and players:
        player = players.pop(0)
        print(f"Trying player: {player}")
        guess_succeeded = guesser.execute_guess(player.full_name)

    if not guess_succeeded:
        raise Exception('Failed to submit a valid guess in the UI')

    # Allow page to load for a sec and then scrape the feedback
    sleep(1)
    guess_feedback = guesser.get_most_recent_guess_feedback()

    # Check to see if we've solved the puzzle, or update the context for the next guess based on the feedback
    if guess_feedback.player_name_feedback.status is AttributeStatus.CORRECT:
        solved = True
        print(f"SOLVED in {attempts} attempts! Correct answer: {player.full_name}")
    else:
        game_context = map_feedback_to_context(guess_feedback, game_context)
