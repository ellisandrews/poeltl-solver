from operator import attrgetter
from time import sleep

from sqlalchemy import create_engine

from poeltl.guess.feedback import AttributeStatus

from .guess.context import GameContext
from .guess.mapping import map_feedback_to_context
from .guesser import Guesser
from .query import build_query, execute_query


# Connect to the database
engine = create_engine('postgresql://postgres@localhost/poeltl', echo=True)

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

    # Query the database for a possible player to guess based on known context
    query = build_query(game_context)
    players = execute_query(engine, query)
    
    # TODO: Implement a retry loop using this list of players if some of these players can't be found on the site
    player = players[0]

    # Make the guess and scrape the feedback
    guesser.execute_guess(player.full_name)
    sleep(1)
    guess_feedback = guesser.get_most_recent_guess_feedback()

    # Check to see if we've solved the puzzle, or update the context for the next guess based on the feedback
    if guess_feedback.player_name_feedback.status is AttributeStatus.CORRECT:
        solved = True
        print(f"SOLVED in {attempts} attempts! Correct answer: {guess_feedback.player_name_feedback.value}")
    else:
        game_context = map_feedback_to_context(guess_feedback, game_context)
