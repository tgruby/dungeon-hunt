import uuid
import game_play
from game_play import images, screen, db, characters, set_game_mode
import dungeon


def process(game, action):
    # Create game, the hero, and dungeon to start the game.  Then
    # set the controller to the town.
    if action is None:
        print("creating character!!!")
        game = game_play.Game(str(uuid.uuid4()))
        game.character = characters.Character(characters.warrior)
        game.dungeon = dungeon.Dungeon()
        game.current_controller = 'game_play.start_game'
        db.save_game(game.game_id, game)

        contents = "The city of Thordon was once a great city, with unimaginable wealth and riches. So much so that " \
                   "to protect their piles of gold they cut deep into the mountain a labyrinth. This maze of " \
                   "corridors and rooms were heavily guarded and laden with traps discouraging the best of thieves. " \
                   "All was well until the dragon came. She came screeching from the sky, her fire laid waste to the " \
                   "town and death was everywhere. She made the labyrinth her home, and as the years went by, " \
                   "wild and evil things moved in. Only a small shell of a town now remains, waiting... hoping… " \
                   "for a hero to free Thordon from its curse and return it to its glory. "

        return screen.paint_one_pane(
            title_image=images.intro_scroll,
            contents=contents,
            contents_image=None,
            commands="Please provide your gamer-tag (for display on the leaderboard):",
            sound=None,
            delay=0,
            interaction_type='enter_press',
            animation=None,
            game_id=game.game_id
        )

    else:
        # Record the name of the character and move forward.
        game.gamer_tag = action
        db.save_game(game.game_id, game)
        game.current_controller = 'game_play.set_game_mode'
        return set_game_mode.process(game, None)
