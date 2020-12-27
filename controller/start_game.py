import db
import uuid
from view import screen, images
from model import characters, games


def process(game, action):
    # Create game, the hero, and dungeon to start the game.  Then
    # set the controller to the town.
    print("creating character!!!")
    game = games.Game(str(uuid.uuid4()))
    game.character = characters.Character(game, characters.warrior)
    game.current_controller = 'town'
    db.save_game(game.game_id, game)
    return screen.paint_one_pane(
        title_image=images.title_1,
        contents="The town of Thordon's renowned catacombs have been laid waste by a treacherous red dragon.  The "
                 "catacombs "
        "had served as a place for both the town dead as well as their treasured secrets from the days of old where "
        "dwarf gold flowed out of the mountain. As the dragon has made it's home in the catacombs, it has slowly "
        "filled with wild animals and more evil things.  Recently, monsters have been leaving the dungeon at night "
        "to drag away town people.  The town is desperate for someone to save them from this deadly decline.  Will you "
        "be their hero?",
        contents_image=None,
        commands='Press any key...',
        sound=None,
        delay=0,
        interaction_type='key_press',
        animation=None,
        game_id=game.game_id
    )