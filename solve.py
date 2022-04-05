from time import sleep

from sqlalchemy import create_engine

from poeltl.guess.context import GameContext
from poeltl.guess.feedback import AttributeStatus
from poeltl.guess.guesser import Guesser
from poeltl.guess.mapping import map_feedback_to_context
from poeltl.guess.query_manager import QueryManager


if __name__ == '__main__':

    # Connect to the database
    engine = create_engine('postgresql://postgres@localhost/poeltl')

    # Instantiate long-lived objects
    query_manager = QueryManager(engine)
    game_context = GameContext()
    guesser = Guesser()

    # Launch a web browser and navigate to the game site
    guesser.navigate_to_poeltl_site()

    # Execute main game loop until the game is solved or out of attempts
    solved = False
    attempts = 0

    while not solved and attempts < 8:

        attempts += 1
        print(f"Beginning attempt {attempts}")

        # Query the database for possible players to guess based on known context
        query = query_manager.build_query(game_context)
        players = query_manager.execute_query(query)
        
        # Try players one by one until a successful guess is submitted
        guess_succeeded = False
        while not guess_succeeded and players:
            player = players.pop(0)
            print(f"Trying player: {player}")
            guess_succeeded = guesser.execute_guess(player.full_name)

        if not guess_succeeded:
            raise Exception('Failed to submit a valid guess in the UI')

        # Allow page to load for a bit and then scrape the feedback
        sleep(1)
        guess_feedback = guesser.get_most_recent_guess_feedback()

        # Check to see if the puzzle is solved or update the context for the next guess based on the feedback
        if guess_feedback.player_name_feedback.status is AttributeStatus.CORRECT:
            solved = True
            print(f"SOLVED in {attempts} attempts! Correct answer: {player.full_name}")
        else:
            game_context = map_feedback_to_context(guess_feedback, game_context)
