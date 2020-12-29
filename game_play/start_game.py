import uuid
import town
import game_play
from game_play import images, screen, db, characters


def process(game, action):
    # Create game, the hero, and dungeon to start the game.  Then
    # set the controller to the town.
    if action is None:
        print("creating character!!!")
        game = game_play.Game(str(uuid.uuid4()))
        game.character = characters.Character(game, characters.warrior)
        game.current_controller = 'game_play.start_game'
        db.save_game(game.game_id, game)

        contents = "“Yeah, well someday, I’ll be something big!!!” you yell as you slam the door to " \
                   "your parents peasant hovel.  So sick of everyone... let me be me. When is that going to start? " \
                   "Mum and da are always saying, \"Be like uncle Erb...\", well uncle Erb died a lonely peasant. Not for " \
                   "me bro, not for me. You run into the town square where a scroll catches " \
                   "your eye.  Nailed to the town post, usually reserved for hanging notices, this one has a gold flare " \
                   "to it.  Dang, wish you knew how to read.  After a few minutes of intense concentration, " \
                   "you make out: “Thordon... Adventures!”.  That's It!  I’ll show them! I’ll become a famous " \
                   "adventurer in the town of Thordon!  Where there is always another dungeon, gold, and a place to make " \
                   "your name!"

        return screen.paint_one_pane(
            title_image=images.intro_scroll,
            contents= contents,
            contents_image=None,
            commands="What is your character's name?",
            sound=None,
            delay=0,
            interaction_type='enter_press',
            animation=None,
            game_id=game.game_id
        )

    else:
        # Record the name of the character and move forward.
        game.character.name = action
        db.save_game(game.game_id, game)
        game.current_controller = 'town'
        return town.process(game, None)
